# utils.py
import sys
from termcolor import colored
import os
import re

def display_message(message, message_type="default"):
    """Display a formatted message based on type"""
    if message_type == "error":
        print(colored(f"❌ ERROR: {message}", "red", attrs=["bold"]))
    elif message_type == "warning":
        print(colored(f"⚠️  WARNING: {message}", "yellow"))
    elif message_type == "success":
        print(colored(f"✅ SUCCESS: {message}", "green"))
    elif message_type == "info":
        print(colored(f"ℹ️  {message}", "cyan"))
    elif message_type == "command":
        print(colored(f"$ {message}", "blue"))
    elif message_type == "output":
        print(colored(f"{message}", "white"))
    elif message_type == "title":
        width = os.get_terminal_size().columns
        print(colored("=" * width, "blue"))
        print(colored(f"{message.center(width)}", "blue", attrs=["bold"]))
        print(colored("=" * width, "blue"))
    else:
        print(message)

def format_code_for_display(code, filename):
    """Format code snippet for terminal display"""
    # Handle None code
    if code is None:
        code = "(empty file)"
        
    # Determine language from filename
    extension = os.path.splitext(filename)[1].lower()
    language_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.jsx': 'JavaScript (React)',
        '.ts': 'TypeScript',
        '.tsx': 'TypeScript (React)',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.json': 'JSON',
        '.md': 'Markdown',
        '.sh': 'Shell',
        '.bash': 'Bash',
        '.sql': 'SQL',
        '.yml': 'YAML',
        '.yaml': 'YAML',
        '.go': 'Go',
        '.rs': 'Rust',
        '.java': 'Java',
        '.c': 'C',
        '.cpp': 'C++',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.vue': 'Vue'
    }
    
    language = language_map.get(extension, 'Code')
    
    # Format header
    header = f" {language} "
    width = os.get_terminal_size().columns - 2  # Account for borders
    padding = width - len(header)
    left_padding = padding // 2
    right_padding = padding - left_padding
    
    print(colored("┌" + "─" * width + "┐", "blue"))
    print(colored("│" + " " * left_padding + header + " " * right_padding + "│", "blue", attrs=["bold"]))
    print(colored("├" + "─" * width + "┤", "blue"))
    
    # Display code with line numbers (limited to 15 lines)
    lines = code.split('\n')
    display_lines = lines[:15]  # Limit to 15 lines for preview
    
    for i, line in enumerate(display_lines):
        line_num = colored(f"{i+1:3d} ", "grey")
        print(colored("│", "blue") + line_num + line + " " * (width - len(line) - 4) + colored("│", "blue"))
    
    # If code was truncated
    if len(lines) > 15:
        omitted = len(lines) - 15
        print(colored("│", "blue") + colored(f" ... {omitted} more lines omitted ...", "yellow").center(width) + colored("│", "blue"))
    
    print(colored("└" + "─" * width + "┘", "blue"))

def get_file_type(filename):
    """Get the type of file based on extension"""
    extension = os.path.splitext(filename)[1].lower()
    
    if extension in ['.py']:
        return 'python'
    elif extension in ['.js', '.jsx', '.ts', '.tsx']:
        return 'javascript'
    elif extension in ['.html']:
        return 'html'
    elif extension in ['.css', '.scss', '.sass']:
        return 'css'
    elif extension in ['.json']:
        return 'json'
    elif extension in ['.md', '.markdown']:
        return 'markdown'
    elif extension in ['.yml', '.yaml']:
        return 'yaml'
    elif extension in ['.sh', '.bash']:
        return 'shell'
    elif extension in ['.sql']:
        return 'sql'
    elif extension in ['.go']:
        return 'go'
    elif extension in ['.rs']:
        return 'rust'
    elif extension in ['.java']:
        return 'java'
    elif extension in ['.c', '.cpp', '.h', '.hpp']:
        return 'c'
    elif extension in ['.rb']:
        return 'ruby'
    elif extension in ['.php']:
        return 'php'
    else:
        return 'text'

def get_keyword_context(content, keyword, context_lines=3):
    """Extract context around a keyword in file content"""
    lines = content.split('\n')
    matches = []
    
    for i, line in enumerate(lines):
        if keyword.lower() in line.lower():
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            context = '\n'.join(lines[start:end])
            matches.append({
                'line_number': i + 1,
                'context': context
            })
    
    return matches

def parse_file_path(file_path):
    """Parse a file path into components"""
    path = os.path.normpath(file_path)
    dirname = os.path.dirname(path)
    basename = os.path.basename(path)
    filename, extension = os.path.splitext(basename)
    
    return {
        'path': path,
        'dirname': dirname,
        'basename': basename,
        'filename': filename,
        'extension': extension
    }

def truncate_text(text, max_length=100):
    """Truncate text to a maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def extract_imports(content, file_type):
    """Extract import statements from code"""
    imports = []
    
    if file_type == 'python':
        # Match Python imports
        import_pattern = r'^(?:from\s+[\w.]+\s+import\s+(?:[\w.]+(?:\s+as\s+\w+)?(?:\s*,\s*[\w.]+(?:\s+as\s+\w+)?)*)|import\s+(?:[\w.]+(?:\s+as\s+\w+)?(?:\s*,\s*[\w.]+(?:\s+as\s+\w+)?)*))$'
        imports = re.findall(import_pattern, content, re.MULTILINE)
    elif file_type in ['javascript', 'typescript']:
        # Match JS/TS imports
        import_pattern = r'^(?:import\s+.+\s+from\s+[\'"][\w./]+[\'"]|const\s+\w+\s*=\s*require\([\'"][\w./]+[\'"]).*$'
        imports = re.findall(import_pattern, content, re.MULTILINE)
    
    return imports

def extract_functions(content, file_type):
    """Extract function definitions from code"""
    functions = []
    
    if file_type == 'python':
        # Match Python functions
        pattern = r'^def\s+(\w+)\s*\(([^)]*)\)'
        matches = re.findall(pattern, content, re.MULTILINE)
        for name, params in matches:
            functions.append({
                'name': name,
                'params': params.strip()
            })
    elif file_type in ['javascript', 'typescript']:
        # Match JS/TS functions
        pattern = r'(?:function\s+(\w+)\s*\(([^)]*)\)|const\s+(\w+)\s*=\s*(?:function)?\s*\(([^)]*)\)|(\w+)\s*:\s*function\s*\(([^)]*)\))'
        matches = re.findall(pattern, content, re.MULTILINE)
        for match in matches:
            # Process different function formats
            if match[0]:  # Standard function
                functions.append({
                    'name': match[0],
                    'params': match[1].strip()
                })
            elif match[2]:  # Const function
                functions.append({
                    'name': match[2],
                    'params': match[3].strip()
                })
            elif match[4]:  # Object method
                functions.append({
                    'name': match[4],
                    'params': match[5].strip()
                })
    
    return functions

def extract_classes(content, file_type):
    """Extract class definitions from code"""
    classes = []
    
    if file_type == 'python':
        # Match Python classes
        pattern = r'^class\s+(\w+)(?:\(([^)]*)\))?:'
        matches = re.findall(pattern, content, re.MULTILINE)
        for name, inheritance in matches:
            classes.append({
                'name': name,
                'inheritance': inheritance.strip()
            })
    elif file_type in ['javascript', 'typescript']:
        # Match JS/TS classes
        pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?'
        matches = re.findall(pattern, content, re.MULTILINE)
        for name, inheritance in matches:
            classes.append({
                'name': name,
                'inheritance': inheritance.strip()
            })
    
    return classes

def detect_dependency_manager(project_path):
    """Detect which dependency manager is used in the project"""
    # Check for package.json (npm/yarn)
    if os.path.exists(os.path.join(project_path, 'package.json')):
        if os.path.exists(os.path.join(project_path, 'yarn.lock')):
            return 'yarn'
        else:
            return 'npm'
    
    # Check for requirements.txt (pip)
    if os.path.exists(os.path.join(project_path, 'requirements.txt')):
        return 'pip'
    
    # Check for Pipfile (pipenv)
    if os.path.exists(os.path.join(project_path, 'Pipfile')):
        return 'pipenv'
    
    # Check for setup.py (setuptools)
    if os.path.exists(os.path.join(project_path, 'setup.py')):
        return 'setuptools'
    
    # Check for poetry
    if os.path.exists(os.path.join(project_path, 'pyproject.toml')):
        with open(os.path.join(project_path, 'pyproject.toml'), 'r') as f:
            if '[tool.poetry]' in f.read():
                return 'poetry'
    
    return 'unknown'

def detect_project_type(project_path):
    """Detect the type of project based on files and structure"""
    # Check for React
    if os.path.exists(os.path.join(project_path, 'package.json')):
        with open(os.path.join(project_path, 'package.json'), 'r') as f:
            content = f.read()
            if '"react"' in content:
                if '"next"' in content:
                    return 'nextjs'
                return 'react'
            elif '"vue"' in content:
                return 'vue'
            elif '"angular"' in content:
                return 'angular'
            else:
                return 'node'
    
    # Check for Django
    if os.path.exists(os.path.join(project_path, 'manage.py')):
        return 'django'
    
    # Check for Flask
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    if 'from flask import' in content:
                        return 'flask'
                    if 'from fastapi import' in content:
                        return 'fastapi'
    
    # Check for other Python projects
    if os.path.exists(os.path.join(project_path, 'setup.py')) or \
       os.path.exists(os.path.join(project_path, 'requirements.txt')) or \
       os.path.exists(os.path.join(project_path, 'pyproject.toml')):
        return 'python'
    
    return 'unknown'

def sanitize_input(input_text):
    """Sanitize user input to prevent command injection"""
    # Remove shell special characters
    sanitized = re.sub(r'[;&|><$`\\]', '', input_text)
    return sanitized