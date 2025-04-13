#!/usr/bin/env python
# agent.py
import os
import argparse
import json
from pathlib import Path
from dotenv import load_dotenv
import sys
import re
import shutil

try:
    # Try to import from the package first (when installed)
    from legion_code_generator.context import ProjectContext
    from legion_code_generator.executor import CommandExecutor
    from legion_code_generator.llm import LLMInterface
    from legion_code_generator.utils import display_message, format_code_for_display
    from legion_code_generator.prompts import FEATURE_IMPLEMENTATION_PROMPT
except ImportError:
    # Fall back to relative imports (when running from source)
    try:
        from context import ProjectContext
        from executor import CommandExecutor
        from llm import LLMInterface
        from utils import display_message, format_code_for_display
        from prompts import FEATURE_IMPLEMENTATION_PROMPT
    except ImportError:
        # Handle case for running from wrapper script or other location
        import sys
        import os
        # Add the parent directory to the path
        sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
        from legion_code_generator.context import ProjectContext
        from legion_code_generator.executor import CommandExecutor
        from legion_code_generator.llm import LLMInterface
        from legion_code_generator.utils import display_message, format_code_for_display
        from legion_code_generator.prompts import FEATURE_IMPLEMENTATION_PROMPT

# Load environment variables from .env file (optional now)
load_dotenv()

class CodingAgent:
    def __init__(self, project_path=None):
        # Initialize components
        self.context = ProjectContext(project_path)
        self.executor = CommandExecutor(self.context)
        
        # Initialize LLM interface - this will now prompt for API credentials
        self.llm = LLMInterface()
        
        # Conversation history for context
        self.history = []
            
    def initialize_project(self, project_name, project_type):
        """Initialize a new project with specified structure"""
        display_message(f"Initializing new {project_type} project: {project_name}", "info")
        
        # Create project directory if it doesn't exist
        project_path = Path(project_name)
        if not project_path.exists():
            project_path.mkdir()
            
        # Set project path in context
        self.context.set_project_path(project_path)
        
        # Generate project structure based on type
        prompt = f"""Create a standard project structure for a {project_type} project.
Do not create a root folder named {project_name} - assume the files will be placed directly in the project directory.
Only output a JSON array of files and folders to create. Each file should include its path and content."""
        
        response = self.llm.generate(prompt)
        
        try:
            # Parse the file structure from LLM response
            file_structure = self.llm.extract_json(response)
            
            # Create the file structure
            for item in file_structure:
                # Check if the path includes a root folder with the project name and remove it
                item_path = item["path"]
                if item_path.startswith(f"{project_name}/") or item_path.startswith(f"{project_name}\\"):
                    item_path = item_path[len(project_name)+1:]  # +1 for the slash
                    display_message(f"Removing project name prefix from path: {item['path']} -> {item_path}", "info")
                    item["path"] = item_path
                
                if "content" in item:
                    # It's a file
                    file_path = project_path / item["path"]
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    # Check if content is None and replace with empty string
                    content = item["content"] if item["content"] is not None else ""
                    with open(file_path, 'w') as f:
                        f.write(content)
                    display_message(f"Created file: {item['path']}", "success")
                else:
                    # It's a directory
                    dir_path = project_path / item["path"]
                    dir_path.mkdir(parents=True, exist_ok=True)
                    display_message(f"Created directory: {item['path']}", "success")
            
            # Verify critical files are in the correct location
            has_nested_structure = False
            if project_type.lower() in ["node", "javascript", "typescript", "react", "vue", "angular"]:
                # Check for package.json in the project root
                pkg_file = project_path / "package.json"
                
                # Check for a nested structure
                project_subdir = project_path / project_name
                nested_pkg_file = project_subdir / "package.json"
                
                if not pkg_file.exists() and project_subdir.exists() and project_subdir.is_dir() and nested_pkg_file.exists():
                    has_nested_structure = True
                    display_message(f"Warning: Found nested project structure. package.json is in {project_name}/{project_name} instead of {project_name}/", "warning")
                    display_message("Attempting to fix the structure...", "info")
                    
                    # Fix the structure by moving files up one level
                    for item in project_subdir.iterdir():
                        target = project_path / item.name
                        # Don't overwrite existing files
                        if not target.exists():
                            if item.is_file():
                                with open(item, 'rb') as src_file:
                                    with open(target, 'wb') as dest_file:
                                        dest_file.write(src_file.read())
                                display_message(f"Moved file: {item.name} to project root", "success")
                            else:
                                # For directories, use recursive copy
                                shutil.copytree(item, target)
                                display_message(f"Moved directory: {item.name} to project root", "success")
                    
                    # Refresh project structure after fixing
                    self.context.refresh_project_structure()
            
            # Install dependencies if applicable
            if project_type.lower() in ["node", "javascript", "typescript", "react", "vue", "angular"]:
                # Check if package.json exists before running npm install
                pkg_file = project_path / "package.json"
                display_message(f"Checking for package.json at: {pkg_file.absolute()}", "info")
                
                if pkg_file.exists():
                    display_message(f"Package.json found. Size: {pkg_file.stat().st_size} bytes", "info")
                    # Verify the file is valid JSON
                    try:
                        with open(pkg_file, 'r') as f:
                            pkg_content = f.read()
                            json.loads(pkg_content)
                        display_message("Package.json is valid JSON. Proceeding with npm install.", "info")
                        self.executor.run_command("npm install")
                    except json.JSONDecodeError:
                        display_message("Package.json exists but contains invalid JSON. Skipping npm install.", "warning")
                    except Exception as e:
                        display_message(f"Error reading package.json: {str(e)}", "error")
                else:
                    display_message("No package.json found. Skipping dependency installation.", "info")
            elif project_type.lower() in ["python", "flask", "django", "fastapi"]:
                # Check if requirements.txt exists before trying to install from it
                req_file = project_path / "requirements.txt"
                if req_file.exists():
                    self.executor.run_command("pip install -r requirements.txt")
                else:
                    display_message("No requirements.txt found. Skipping dependency installation.", "info")
                
            display_message(f"{project_type} project {project_name} initialized successfully!", "success")
            
        except Exception as e:
            display_message(f"Error initializing project: {str(e)}", "error")
    
    def update_project(self, prompt):
        """Update the project based on a user prompt"""
        # Add the prompt to history
        self.history.append({"role": "user", "content": prompt})
        
        # Check if we have a valid project to update
        structure = self.context.get_project_structure()
        if not structure:
            display_message("Error: No project structure found. Please initialize a project first with 'init <project_name> <project_type>'", "error")
            return
            
        # Check if this might be a web project requiring package.json
        is_web_feature = any(keyword in prompt.lower() for keyword in ["navigation", "navbar", "header", "footer", "component", "react", "vue", "angular", "javascript", "html", "css"])
        has_package_json = os.path.exists(os.path.join(self.context.project_path, "package.json"))
        
        if is_web_feature and not has_package_json:
            display_message("Warning: Your request appears to be for a web project, but there's no package.json file.", "warning")
            display_message("This might cause errors if the feature requires npm packages. Consider initializing a proper web project first.", "info")
            
            # Ask for confirmation before proceeding
            confirmation = input("\nDo you still want to proceed? (y/n): ")
            if confirmation.lower() != 'y':
                display_message("Operation cancelled by user.", "info")
                return
        
        # Get content of relevant files based on the request
        relevant_files = self.context.get_relevant_files(prompt)
        file_contents = ""
        for file_path in relevant_files:
            content = self.context.get_file_content(file_path)
            if content:
                file_contents += f"\nFile: {file_path}\n```\n{content}\n```\n"
        
        # Create the system prompt manually instead of using format to avoid issues with braces in JSON
        system_prompt = """
You are a terminal-based coding assistant specialized in implementing features in existing projects.
Based on the project structure and the user's feature request, determine what files need to be modified or created.

Project structure:
""" + json.dumps(structure, indent=2) + """

Feature requested: """ + prompt + """

For selected relevant files, here are their contents:
""" + file_contents + """

Return your response as a JSON array of files to create or modify, with each file containing:
- "path": The relative path of the file
- "content": The complete content of the file after your changes

Format:
[
  {
    "path": "path/to/file.ext",
    "content": "Complete file content including your changes"
  }
]

Ensure your implementation:
1. Follows the project's existing patterns and coding style
2. Includes all necessary imports and dependencies
3. Provides complete functional code (not pseudocode)
4. Makes minimal changes to existing functionality unless specified

IMPORTANT: Your response MUST be a valid JSON array. Do not include any explanations outside the JSON array.
"""
        
        # Generate the response
        display_message("Generating response for project update...", "info")
        response = self.llm.generate(
            user_prompt="Please implement the following feature: " + prompt,
            system_prompt=system_prompt,
        )
        
        # Debug: Display the raw response
        display_message("Received response from LLM. Extracting JSON...", "info")
        
        try:
            # Parse the file changes from LLM response
            file_changes = self.llm.extract_json(response)
            
            if not file_changes or not isinstance(file_changes, list) or len(file_changes) == 0:
                raise ValueError("Empty or invalid JSON structure returned by LLM")
            
            # Apply the changes
            project_path = self.context.project_path
            for item in file_changes:
                if "path" not in item or "content" not in item:
                    display_message(f"Skipping invalid item in response: {item}", "warning")
                    continue
                    
                file_path = project_path / item["path"]
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Check if it's a new file or modification
                is_new = not file_path.exists()
                
                # Handle None content
                content = item["content"] if item["content"] is not None else ""
                
                # Write the content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                if is_new:
                    display_message(f"Created new file: {item['path']}", "success")
                else:
                    display_message(f"Updated file: {item['path']}", "success")
            
            # Check if we need to install any dependencies
            response_text = json.dumps(file_changes)
            web_deps = re.findall(r'import\s+.*?\s+from\s+[\'"]([a-zA-Z0-9\-_]+)[\'"]', response_text)
            py_deps = re.findall(r'import\s+([a-zA-Z0-9\-_]+)', response_text)
            
            has_pkg_json = os.path.exists(os.path.join(project_path, "package.json"))
            has_req_txt = os.path.exists(os.path.join(project_path, "requirements.txt"))
            
            if web_deps and has_pkg_json:
                known_builtin_modules = ["react", "react-dom", "react-router-dom", "react-router", "vue", "angular", "svelte",
                                         "path", "fs", "os", "crypto", "child_process", "http", "https", "express",
                                         "./", "../", "/"]
                                         
                external_deps = [dep for dep in web_deps if not any(dep.startswith(builtin) for builtin in known_builtin_modules)]
                
                if external_deps:
                    display_message(f"Detected possible npm dependencies: {', '.join(external_deps)}", "info")
                    display_message("Would you like to install them? (y/n): ", "info", end="")
                    if input().lower() == 'y':
                        self.executor.run_command(f"npm install --save {' '.join(external_deps)}")
                        
            elif py_deps and has_req_txt:
                known_builtin_modules = ["os", "sys", "datetime", "json", "re", "math", "random", "time", "pathlib",
                                        "typing", "collections", "functools", "itertools", "logging"]
                                        
                external_deps = [dep for dep in py_deps if dep not in known_builtin_modules]
                
                if external_deps:
                    display_message(f"Detected possible Python dependencies: {', '.join(external_deps)}", "info")
                    display_message("Would you like to add them to requirements.txt? (y/n): ", "info", end="")
                    if input().lower() == 'y':
                        with open(os.path.join(project_path, "requirements.txt"), 'a') as f:
                            for dep in external_deps:
                                f.write(f"{dep}\n")
                        display_message("Added dependencies to requirements.txt. You may want to run 'pip install -r requirements.txt'", "success")
            
            display_message("Project updated successfully!", "success")
            
        except Exception as e:
            display_message(f"Error updating project: {str(e)}", "error")
            
    def run_command(self, command):
        """Run a shell command in the project directory"""
        self.executor.run_command(command)
        
    def explain_project(self):
        """Generate an explanation of the current project"""
        structure = self.context.get_project_structure()
        if not structure:
            display_message("Error: No project structure found. Please initialize a project first with 'init <project_name> <project_type>'", "error")
            return
            
        prompt = f"Analyze the following project structure and provide a clear explanation of what this project does, its components, and how they interact:\n\n{json.dumps(structure, indent=2)}"
        response = self.llm.generate(prompt)
        display_message(response, "info")
    
    def interactive_mode(self):
        """Start an interactive session with the agent"""
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table
        from rich.text import Text
        from rich.prompt import Prompt
        from rich.layout import Layout
        from rich.box import ROUNDED
        
        console = Console()
        
        # Display header with Rich panel
        console.print(Panel(
            Text("💥 LEGION AI CODE GENERATOR 💥", justify="center"),
            border_style="cyan",
            box=ROUNDED,
            style="bold magenta",
            expand=False
        ))
        
        # Display API info in a table
        api_table = Table(show_header=False, box=ROUNDED, border_style="blue")
        api_table.add_column("Property", style="bold cyan")
        api_table.add_column("Value", style="green")
        api_table.add_row("API Type", f"{self.llm.api_type.upper()}")
        api_table.add_row("Model", f"{self.llm.model}")
        console.print(api_table)
        
        # Help panel
        help_panel = Panel(
            "[bold cyan]Commands:[/bold cyan]\n"
            "  [yellow]init[/yellow] <project_name> <project_type> - Initialize a new project\n"
            "  [yellow]run[/yellow] <command> - Run a shell command in the project directory\n"
            "  [yellow]explain[/yellow] - Generate an explanation of the current project\n"
            "  [yellow]api[/yellow] - Show information about the configured API\n"
            "  [yellow]help[/yellow] - Show this help message\n"
            "  [yellow]exit[/yellow] - Exit the program\n"
            "  [cyan]<any other text>[/cyan] - Interpreted as a feature request",
            title="Help",
            border_style="blue",
            box=ROUNDED,
            expand=False
        )
        
        display_message("Type 'exit' to quit, 'help' for available commands", "info", flush=True)
        
        while True:
            try:
                # Flush message buffer before showing the prompt, but without creating empty message
                from legion_code_generator.utils import _flush_message_buffers
                _flush_message_buffers()
                
                user_input = Prompt.ask("\n[bold green]legion>[/bold green]")
                
                if user_input.lower() in ["exit", "quit"]:
                    display_message("Exiting Legion Code Generator. Goodbye!", "info", flush=True)
                    break
                    
                elif user_input.lower() == "help":
                    console.print(help_panel)
                
                elif user_input.lower().startswith("init "):
                    parts = user_input.split(maxsplit=2)
                    if len(parts) != 3:
                        display_message("Error: 'init' command requires a project name and type. Example: 'init my_project react'", "error", flush=True)
                    else:
                        _, project_name, project_type = parts
                        self.initialize_project(project_name, project_type)
                
                elif user_input.lower().startswith("run "):
                    command = user_input[4:]
                    self.run_command(command)
                
                elif user_input.lower() == "explain":
                    self.explain_project()
                    
                elif user_input.lower() == "api":
                    api_info = self.llm.get_api_info()
                    api_status_table = Table(show_header=False, box=ROUNDED, border_style="blue")
                    api_status_table.add_column("Property", style="bold cyan")
                    api_status_table.add_column("Value", style="green")
                    api_status_table.add_row("API Type", api_info['type'])
                    api_status_table.add_row("Model", api_info['model'])
                    api_status_table.add_row("Key Status", 'Configured' if api_info['key_status'] else 'Not configured')
                    console.print(api_status_table)
                
                else:
                    # Treat as a feature request
                    self.update_project(user_input)
                    
                # No need to flush empty messages
                _flush_message_buffers()
                    
            except KeyboardInterrupt:
                display_message("\nExiting Legion Code Generator. Goodbye!", "info", flush=True)
                break
                
            except Exception as e:
                display_message(f"Error: {str(e)}", "error", flush=True)


def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(description="Legion Code Generator - A terminal-based AI coding agent")
    
    parser.add_argument("--init", nargs=2, metavar=("PROJECT_NAME", "PROJECT_TYPE"), 
                        help="Initialize a new project with the specified name and type")
    parser.add_argument("--project", type=str, help="Path to the project directory")
    parser.add_argument("--request", type=str, help="Feature request to update the project")
    parser.add_argument("--command", type=str, help="Shell command to run in the project directory")
    parser.add_argument("--explain", action="store_true", help="Generate an explanation of the current project")
    parser.add_argument("--api-key", type=str, help="API key for the LLM service")
    parser.add_argument("--api-type", type=str, choices=["openai", "gemini", "azure"], default="openai", 
                       help="Type of LLM API to use (default: openai)")
    parser.add_argument("--version", action="version", version="legion-code-generator 0.1.0")
    
    args = parser.parse_args()
    
    # Set API key from command line argument if provided
    if args.api_key:
        os.environ["OPENAI_API_KEY"] = args.api_key
        
    # Set API type from command line argument if provided
    if args.api_type:
        os.environ["API_TYPE"] = args.api_type
    
    agent = CodingAgent(args.project)
    
    # Process command line arguments
    if args.init:
        project_name, project_type = args.init
        agent.initialize_project(project_name, project_type)
    elif args.request:
        agent.update_project(args.request)
    elif args.command:
        agent.run_command(args.command)
    elif args.explain:
        agent.explain_project()
    else:
        # No specific command provided, start interactive mode
        agent.interactive_mode()


if __name__ == "__main__":
    main() 