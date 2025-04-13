# context.py
import os
from pathlib import Path
import json

try:
    from legion_code_generator.utils import display_message
except ImportError:
    from utils import display_message

class ProjectContext:
    def __init__(self, project_path=None):
        """Initialize project context with optional project path"""
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.project_structure = {}
        self.file_contents = {}
        
        # Initialize project structure if path exists
        if self.project_path.exists():
            self.refresh_project_structure()
    
    def set_project_path(self, path):
        """Set or update the project path"""
        self.project_path = Path(path)
        self.refresh_project_structure()
    
    def refresh_project_structure(self):
        """Scan the project directory and update the structure"""
        display_message(f"Refreshing project structure for path: {self.project_path}", "info")
        
        # Check if the project path exists
        if not self.project_path.exists():
            display_message(f"Warning: Project path does not exist: {self.project_path}", "warning")
            self.project_structure = []
            self.file_contents = {}
            return
            
        if not self.project_path.is_dir():
            display_message(f"Warning: Project path is not a directory: {self.project_path}", "warning")
            self.project_structure = []
            self.file_contents = {}
            return
            
        # Count files before scanning
        file_count_before = len(self._flatten_structure(self.project_structure)) if self.project_structure else 0
        
        # Scan the directory
        self.project_structure = self._scan_directory(self.project_path)
        
        # Count files after scanning
        file_count_after = len(self._flatten_structure(self.project_structure))
        
        # Cache file contents
        self._cache_file_contents()
        
        # Check for package.json specifically
        pkg_json_path = self.project_path / "package.json"
        if pkg_json_path.exists():
            display_message(f"Found package.json in project structure: {pkg_json_path}", "info")
            # Make sure it's in the structure
            if not any("package.json" in item.get("path", "") for item in self._flatten_structure(self.project_structure)):
                display_message("Warning: package.json exists but was not included in project structure!", "warning")
        
        display_message(f"Project structure refreshed. Files before: {file_count_before}, Files after: {file_count_after}", "info")
    
    def _scan_directory(self, directory, relative_to=None):
        """Recursively scan a directory and return its structure"""
        if relative_to is None:
            relative_to = self.project_path
            
        result = []
        
        try:
            # Check explicitly for important files like package.json at the root level
            if directory == self.project_path:
                important_files = ["package.json", "requirements.txt"]
                for filename in important_files:
                    file_path = directory / filename
                    if file_path.exists() and file_path.is_file():
                        display_message(f"Found important file: {filename}", "info")
                        relative_path = file_path.relative_to(relative_to)
                        file_info = {
                            "type": "file",
                            "name": filename,
                            "path": str(relative_path),
                            "extension": file_path.suffix
                        }
                        
                        if self._is_text_file(file_path):
                            if file_path.stat().st_size < 1024 * 1024:
                                file_info["size"] = file_path.stat().st_size
                            else:
                                file_info["size"] = "large"
                        else:
                            file_info["binary"] = True
                            
                        result.append(file_info)
            
            for item in directory.iterdir():
                # Skip hidden files and directories
                if item.name.startswith('.'):
                    continue
                    
                # Skip virtual environments and node_modules
                if item.is_dir() and item.name in ['venv', 'env', 'node_modules', '__pycache__']:
                    continue
                
                # Skip files we've already processed explicitly
                if directory == self.project_path and item.is_file() and item.name in ["package.json", "requirements.txt"]:
                    continue
                    
                relative_path = item.relative_to(relative_to)
                
                if item.is_dir():
                    # It's a directory
                    children = self._scan_directory(item, relative_to)
                    result.append({
                        "type": "directory",
                        "name": item.name,
                        "path": str(relative_path),
                        "children": children
                    })
                else:
                    # It's a file
                    file_info = {
                        "type": "file",
                        "name": item.name,
                        "path": str(relative_path),
                        "extension": item.suffix
                    }
                    
                    # Only include size for binary files or large files
                    if self._is_text_file(item):
                        # Check if file is not too large (> 1MB)
                        if item.stat().st_size < 1024 * 1024:
                            file_info["size"] = item.stat().st_size
                        else:
                            file_info["size"] = "large"
                    else:
                        file_info["binary"] = True
                        
                    result.append(file_info)
        except Exception as e:
            print(f"Error scanning directory {directory}: {str(e)}")
            
        return result
    
    def _is_text_file(self, file_path):
        """Check if a file is a text file based on its extension"""
        text_extensions = [
            '.txt', '.md', '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', 
            '.scss', '.json', '.yaml', '.yml', '.xml', '.csv', '.ini', '.cfg',
            '.conf', '.sh', '.bash', '.zsh', '.env', '.toml', '.rs', '.go',
            '.java', '.c', '.cpp', '.h', '.hpp', '.rb', '.php', '.vue'
        ]
        
        return file_path.suffix.lower() in text_extensions
    
    def _cache_file_contents(self):
        """Cache contents of text files for context"""
        self.file_contents = {}
        
        def process_item(item):
            if item["type"] == "file" and not item.get("binary", False) and item.get("size", 0) != "large":
                try:
                    file_path = self.project_path / item["path"]
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        self.file_contents[item["path"]] = f.read()
                except Exception as e:
                    print(f"Error reading file {item['path']}: {str(e)}")
            elif item["type"] == "directory":
                for child in item["children"]:
                    process_item(child)
        
        for item in self.project_structure:
            process_item(item)
    
    def get_project_structure(self):
        """Get the current project structure"""
        return self.project_structure
    
    def get_file_content(self, file_path):
        """Get the content of a specific file"""
        rel_path = str(Path(file_path).relative_to(self.project_path)) if isinstance(file_path, Path) else file_path
        
        if rel_path in self.file_contents:
            return self.file_contents[rel_path]
        
        # If not in cache, try to read it
        try:
            full_path = self.project_path / rel_path
            if full_path.exists() and full_path.is_file():
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    self.file_contents[rel_path] = content
                    return content
        except Exception as e:
            print(f"Error reading file {rel_path}: {str(e)}")
            
        return None
    
    def write_file(self, file_path, content):
        """Write content to a file and update the cache"""
        rel_path = str(Path(file_path).relative_to(self.project_path)) if isinstance(file_path, Path) else file_path
        full_path = self.project_path / rel_path
        
        # Create parent directories if they don't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the content
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Update cache
        self.file_contents[rel_path] = content
        
        # Refresh structure if it's a new file
        if not any(item["path"] == rel_path for item in self._flatten_structure(self.project_structure)):
            self.refresh_project_structure()
    
    def _flatten_structure(self, structure, result=None):
        """Flatten the nested structure into a list of files"""
        if result is None:
            result = []
            
        for item in structure:
            if item["type"] == "file":
                result.append(item)
            elif item["type"] == "directory":
                self._flatten_structure(item["children"], result)
                
        return result
    
    def get_relevant_files(self, query):
        """Find files that are relevant to a specific query"""
        # Simple relevance check based on filename and extensions
        relevant = []
        query_terms = query.lower().split()
        
        for path, content in self.file_contents.items():
            path_lower = path.lower()
            relevance_score = 0
            
            # Check filename relevance
            for term in query_terms:
                if term in path_lower:
                    relevance_score += 5
            
            # Check content relevance (simple search)
            content_lower = content.lower()
            for term in query_terms:
                if term in content_lower:
                    relevance_score += 1
            
            if relevance_score > 0:
                relevant.append((path, relevance_score))
        
        # Sort by relevance score
        relevant.sort(key=lambda x: x[1], reverse=True)
        
        # Return the paths only
        return [path for path, _ in relevant[:10]]  # Limit to top 10
    
    def to_json(self):
        """Convert the project context to JSON for serialization"""
        return {
            "project_path": str(self.project_path),
            "structure": self.project_structure,
            # Exclude file_contents as it might be too large
        }