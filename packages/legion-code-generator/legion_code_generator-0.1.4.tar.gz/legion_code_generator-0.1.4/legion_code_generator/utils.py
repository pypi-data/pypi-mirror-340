# utils.py
import sys
import os
import re
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.box import ROUNDED

# Initialize Rich console
console = Console()

# Global message buffers for grouping similar messages
_message_buffers = {
    "error": [],
    "warning": [],
    "success": [],
    "info": [],
    "command": [],
    "output": [],
    "default": []
}
_last_message_type = None

def display_message(message, message_type="default", end="\n", flush=False):
    """Display a formatted message based on type using Rich
    
    Args:
        message: The message to display
        message_type: Type of message (error, warning, success, info, command, output, title)
        end: End character
        flush: Force flush all buffered messages
    """
    global _last_message_type, _message_buffers
    
    # Title messages are always displayed immediately
    if message_type == "title":
        # Flush any pending messages first
        _flush_message_buffers()
        
        # For title type, use a special centered format
        console.print(Panel(
            Text(message, justify="center", style="bold blue"),
            border_style="cyan",
            box=ROUNDED,
            style="bold magenta",
            expand=True
        ))
        return
    
    # If message is empty and it's only for flushing, don't add to buffer
    if flush and not message.strip():
        if _last_message_type:
            _flush_message_buffers()
        return
    
    # If message type changed or flush requested, flush the buffer
    if _last_message_type is not None and _last_message_type != message_type or flush:
        _flush_message_buffers()
    
    # Only add non-empty messages to the buffer
    if message.strip() or end != "\n":
        # Add the message to the appropriate buffer
        if message_type in _message_buffers:
            _message_buffers[message_type].append(message)
        else:
            _message_buffers["default"].append(message)
        
        _last_message_type = message_type
    
    # If end is not newline, flush immediately
    if end != "\n":
        _flush_message_buffers()

def _flush_message_buffers():
    """Flush all message buffers, displaying grouped messages in panels"""
    global _last_message_type, _message_buffers
    
    # If no last message type, nothing to flush
    if _last_message_type is None:
        return
    
    # Get the current buffer and message type
    current_buffer = _message_buffers[_last_message_type]
    
    # If the buffer is empty, nothing to do
    if not current_buffer:
        _last_message_type = None
        return
    
    # Filter out empty messages
    current_buffer = [msg for msg in current_buffer if msg.strip()]
    
    # If all messages were empty, nothing to do
    if not current_buffer:
        _message_buffers[_last_message_type] = []
        _last_message_type = None
        return
    
    # Configure styles based on message type
    if _last_message_type == "error":
        title = "❌ ERROR"
        style = "red"
        border_style = "red"
    elif _last_message_type == "warning":
        title = "⚠️ WARNING"
        style = "yellow"
        border_style = "yellow"
    elif _last_message_type == "success":
        title = "✅ SUCCESS"
        style = "green"
        border_style = "green"
    elif _last_message_type == "info":
        title = "ℹ️ INFO"
        style = "cyan"
        border_style = "cyan"
    elif _last_message_type == "command":
        title = "$ Command"
        style = "blue"
        border_style = "blue"
    elif _last_message_type == "output":
        title = "Output"
        style = "white"
        border_style = "white"
    else:
        title = None
        style = "default"
        border_style = "blue"
    
    # Join the messages and create a panel
    if len(current_buffer) == 1:
        # Single message
        panel_content = current_buffer[0]
    else:
        # Multiple messages
        panel_content = "\n".join(current_buffer)
    
    panel = Panel(
        panel_content,
        title=title,
        title_align="left",
        border_style=border_style,
        box=ROUNDED,
        style=style,
        expand=False
    )
    console.print(panel)
    
    # Clear the buffer
    _message_buffers[_last_message_type] = []
    _last_message_type = None

# Add atexit handler to ensure all messages are flushed on program exit
import atexit
atexit.register(_flush_message_buffers)

def format_code_for_display(code, filename):
    """Format code snippet for terminal display using Rich syntax highlighting"""
    # Handle None code
    if code is None:
        code = "(empty file)"
        
    # Determine language from filename
    extension = os.path.splitext(filename)[1].lower()
    language_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.html': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.json': 'json',
        '.md': 'markdown',
        '.sh': 'bash',
        '.bash': 'bash',
        '.sql': 'sql',
        '.yml': 'yaml',
        '.yaml': 'yaml',
        '.go': 'go',
        '.rs': 'rust',
        '.java': 'java',
        '.c': 'c',
        '.cpp': 'cpp',
        '.rb': 'ruby',
        '.php': 'php',
        '.vue': 'html'
    }
    
    lexer = language_map.get(extension, 'text')
    
    # Create title
    title = os.path.basename(filename)
    
    # Create syntax highlighted code with line numbers
    # Truncate to first 15 lines for preview
    lines = code.split('\n')
    display_code = '\n'.join(lines[:15])
    
    # Create syntax object with line numbers
    syntax = Syntax(
        display_code,
        lexer,
        line_numbers=True,
        theme="monokai",
        word_wrap=True
    )
    
    # Create panel with code
    panel = Panel(
        syntax,
        title=title,
        border_style="blue",
        expand=False
    )
    
    # Print the panel
    console.print(panel)
    
    # If code was truncated
    if len(lines) > 15:
        omitted = len(lines) - 15
        console.print(f"[yellow]... {omitted} more lines omitted ...[/yellow]", justify="center")

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