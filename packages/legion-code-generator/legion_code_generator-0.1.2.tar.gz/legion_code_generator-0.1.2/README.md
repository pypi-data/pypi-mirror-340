# Legion Code Generator

A powerful terminal-based AI agent specialized in coding and full-stack project development. This tool helps developers create, modify, and maintain projects through natural language instructions in the terminal.

## Features

- **Project Initialization**: Generate complete project structures for various frameworks and languages
- **Code Generation**: Create files with well-structured code based on natural language descriptions
- **Context-Aware Updates**: Modify existing projects by understanding the current codebase
- **Command Execution**: Run system commands like `npm install` or `pip install` directly
- **Interactive Mode**: Engage in a conversation-like experience for iterative development
- **Multiple LLM Support**: Use either OpenAI or Google's Gemini API

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key or Google Gemini API key

### Install from PyPI

```bash
pip install legion-code-generator
```

### Install from source

1. Clone the repository:
   ```bash
   git clone https://github.com/legionai/legion-code-generator.git
   cd legion-code-generator
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Usage

### Using your API Key

You have several options for providing your API key:

1. **Command-line argument**:
   ```bash
   # For OpenAI API
   legion-code-generator --api-key "your-api-key-here" --api-type openai
   
   # For Gemini API
   legion-code-generator --api-key "your-api-key-here" --api-type gemini
   ```

2. **Environment variable**:
   ```bash
   # For OpenAI (Linux/macOS)
   export OPENAI_API_KEY="your-api-key-here"
   legion-code-generator
   
   # For Gemini (Linux/macOS)
   export OPENAI_API_KEY="your-gemini-api-key-here"
   export BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
   legion-code-generator
   ```

3. **.env file**:
   Create a `.env` file in your working directory with:
   ```
   # For OpenAI
   OPENAI_API_KEY=your-api-key-here
   
   # For Gemini
   OPENAI_API_KEY=your-gemini-api-key-here
   BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
   ```

### Interactive API Selection

If you don't provide an API key or type via command line or environment, Legion Code Generator will prompt you to select between OpenAI and Gemini APIs, and then ask for your API key.

### Command-line Options

```bash
# Initialize a new project
legion-code-generator --init project_name project_type

# Work with an existing project
legion-code-generator --project /path/to/your/project

# Make a specific feature request
legion-code-generator --project /path/to/your/project --request "Add a navigation bar with responsive design"

# Run a shell command in the project context
legion-code-generator --project /path/to/your/project --command "npm install bootstrap"

# Get an explanation of the current project
legion-code-generator --project /path/to/your/project --explain

# Specify the API type
legion-code-generator --api-type gemini --api-key "your-gemini-api-key"

# Start interactive mode (default)
legion-code-generator --project /path/to/your/project
```

### Interactive Mode Commands

Once in interactive mode, you can use the following commands:

- **Initialize a Project**:
  ```
  init my_project react
  ```
  Creates a new React project with appropriate structure and files.

- **Run a Command**:
  ```
  run npm install react-router-dom
  ```
  Executes the command in the project directory.

- **Explain Project**:
  ```
  explain
  ```
  Provides an explanation of the current project structure and components.

- **API Information**:
  ```
  api
  ```
  Displays information about the currently configured API and model.

- **Update Project**:
  Simply type your request in natural language:
  ```
  Add a login page with React Router integration
  ```
  or
  ```
  Create a database schema for user profiles with SQLite
  ```

- **Exit Interactive Mode**:
  ```
  exit
  ```
  or press Ctrl+C

## Examples

### Creating a new React project

```
> legion-code-generator --init myapp react
🤖 Initializing new react project: myapp
✅ Created directory: src
✅ Created file: src/index.js
✅ Created file: src/App.js
✅ Created file: src/App.css
✅ Created file: public/index.html
✅ Created file: package.json
✅ Created file: .gitignore
$ npm install
React project myapp initialized successfully!
```

### Adding a feature to an existing project

```
> legion-code-generator --project ./myapp --request "Add a navigation bar with Home, About and Contact links"
Processing request...
✅ Updated file: src/App.js
✅ Created new file: src/components/Navbar.js
✅ Updated file: src/App.css
```

### Running build commands

```
> legion-code-generator --project ./myapp --command "npm run build"
$ npm run build
Creating an optimized production build...
Build completed successfully!
```

## Development

### Project Structure

```
legion_code_generator/
├── __init__.py      # Package initialization
├── agent.py         # Main entry point and CLI handler
├── context.py       # Project context management
├── llm.py           # LLM integration
├── executor.py      # Command execution
├── utils.py         # Helper functions
└── prompts.py       # LLM prompting templates
```


## Limitations

- The agent requires an internet connection to use OpenAI's or Gemini's API.
- Very large projects might exceed context limits of the LLM.
- The agent cannot debug runtime errors or test the functionality of the code it generates.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- This project uses AI APIs (OpenAI/Gemini) for code generation and understanding.
- Special thanks to the open-source community for inspiration and tools.