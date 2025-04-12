# executor.py
import subprocess
import os
import sys
import platform
import json

try:
    from legion_code_generator.utils import display_message
except ImportError:
    from utils import display_message

class CommandExecutor:
    def __init__(self, context):
        """Initialize command executor with project context"""
        self.context = context
        self.last_command = None
        self.last_result = None
    
    def run_command(self, command):
        """Run a system command in the project directory"""
        self.last_command = command
        
        # Get the project directory
        project_dir = self.context.project_path
        
        # Add special handling for npm commands
        if command.startswith("npm "):
            # Verify npm is installed first
            display_message("Verifying npm installation...", "info")
            try:
                # Check npm version
                if platform.system() == "Windows":
                    npm_check_args = ["cmd.exe", "/c", "npm --version"]
                else:
                    npm_check_args = "npm --version"
                    
                npm_process = subprocess.Popen(
                    npm_check_args,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                
                npm_stdout, npm_stderr = npm_process.communicate()
                
                if npm_process.returncode != 0:
                    display_message("npm is not installed or not in PATH. Please install npm first.", "error")
                    self.last_result = {
                        "stdout": "",
                        "stderr": "npm command not found. Please install npm first.",
                        "return_code": 1
                    }
                    return "npm command not found. Please install npm first."
                else:
                    display_message(f"npm version {npm_stdout.strip()} found", "info")
            except Exception as e:
                display_message(f"Error checking npm: {str(e)}", "error")
        
        # Check for common commands that might fail due to missing files
        if command.startswith("pip install -r "):
            req_file = command.split(" ")[-1]
            req_path = os.path.join(project_dir, req_file)
            if not os.path.exists(req_path):
                error_message = f"Could not open requirements file: No such file or directory: '{req_file}'"
                display_message(f"Error: {error_message}", "error")
                self.last_result = {
                    "stdout": "",
                    "stderr": error_message,
                    "return_code": 1
                }
                return error_message
        elif command.startswith("npm "):
            # Check for package.json when running npm commands
            pkg_path = os.path.join(project_dir, "package.json")
            display_message(f"Checking for package.json at: {pkg_path}", "info")
            
            if not os.path.exists(pkg_path):
                error_message = "Could not read package.json: Error: ENOENT: no such file or directory, open 'package.json'"
                display_message(f"Error: {error_message}", "error")
                display_message("Please initialize a project first with 'init <project_name> <project_type>'", "info")
                display_message("For web projects, try: init my_project react", "info")
                self.last_result = {
                    "stdout": "",
                    "stderr": error_message,
                    "return_code": 1
                }
                return error_message
            else:
                display_message(f"Found package.json ({os.path.getsize(pkg_path)} bytes)", "info")
                # Verify the file is valid JSON
                try:
                    with open(pkg_path, 'r') as f:
                        pkg_content = f.read()
                        json.loads(pkg_content)
                    display_message("package.json is valid JSON", "info")
                except json.JSONDecodeError:
                    display_message("package.json exists but contains invalid JSON", "warning")
                except Exception as e:
                    display_message(f"Error reading package.json: {str(e)}", "error")
        
        # Split the command into parts
        if platform.system() == "Windows":
            # For Windows, use cmd.exe
            args = ["cmd.exe", "/c", command]
            shell = True
        else:
            # For Unix/Linux/Mac
            args = command
            shell = True
        
        try:
            # Run the command
            display_message(f"Running command: {command}", "command")
            
            # Execute the command
            process = subprocess.Popen(
                args,
                shell=shell,
                cwd=project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Use communicate() to avoid deadlocks
            stdout, stderr = process.communicate()
            
            # Print the output
            if stdout:
                print(stdout)
            if stderr:
                print(stderr, file=sys.stderr)
            
            # Store the result
            self.last_result = {
                "stdout": stdout,
                "stderr": stderr,
                "return_code": process.returncode
            }
            
            # Check if the command was successful
            if process.returncode != 0:
                display_message(f"Command failed with return code {process.returncode}", "warning")
                return self.last_result["stderr"]
            else:
                return self.last_result["stdout"]
            
        except Exception as e:
            error_message = f"Error executing command: {str(e)}"
            display_message(error_message, "error")
            self.last_result = {
                "stdout": "",
                "stderr": error_message,
                "return_code": -1
            }
            return error_message
    
    def run_package_install(self, package_manager, packages):
        """Install packages using specified package manager"""
        # Determine the appropriate install command
        if package_manager.lower() == "npm":
            # Check if package.json exists
            pkg_path = os.path.join(self.context.project_path, "package.json")
            if not os.path.exists(pkg_path):
                error_message = "Could not read package.json: Error: ENOENT: no such file or directory, open 'package.json'"
                display_message(f"Error: {error_message}", "error")
                display_message("Please initialize a project first with 'init <project_name> <project_type>'", "info")
                display_message("For web projects, try: init my_project react", "info")
                return error_message
            command = f"npm install {packages}"
        elif package_manager.lower() == "pip":
            command = f"pip install {packages}"
        elif package_manager.lower() == "yarn":
            # Check if package.json exists for yarn as well
            pkg_path = os.path.join(self.context.project_path, "package.json")
            if not os.path.exists(pkg_path):
                error_message = "Could not read package.json: Error: ENOENT: no such file or directory, open 'package.json'"
                display_message(f"Error: {error_message}", "error")
                display_message("Please initialize a project first with 'init <project_name> <project_type>'", "info")
                display_message("For web projects, try: init my_project react", "info")
                return error_message
            command = f"yarn add {packages}"
        else:
            return f"Unsupported package manager: {package_manager}"
        
        # Run the install command
        return self.run_command(command)
    
    def run_build_command(self, build_type):
        """Run build command based on project type"""
        # Determine the appropriate build command
        if build_type.lower() in ["react", "vue", "angular", "node"]:
            # Check if package.json exists before running npm build
            pkg_path = os.path.join(self.context.project_path, "package.json")
            if not os.path.exists(pkg_path):
                error_message = "Could not read package.json: Error: ENOENT: no such file or directory, open 'package.json'"
                display_message(f"Error: {error_message}", "error")
                display_message("Please initialize a project first with 'init <project_name> <project_type>'", "info")
                display_message("For web projects, try: init my_project react", "info")
                return error_message
            command = "npm run build"
        elif build_type.lower() == "python":
            # For Python, we might use different commands depending on the framework
            # Check for common build files
            if (self.context.project_path / "setup.py").exists():
                command = "pip install -e ."
            else:
                return "No standard build process for this Python project"
        else:
            return f"Unsupported build type: {build_type}"
        
        # Run the build command
        return self.run_command(command)
    
    def get_last_result(self):
        """Get the result of the last command execution"""
        return self.last_result