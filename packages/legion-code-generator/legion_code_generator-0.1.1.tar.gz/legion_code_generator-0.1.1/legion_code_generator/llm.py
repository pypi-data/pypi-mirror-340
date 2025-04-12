# llm.py
import os
import json
import re
import getpass
from dotenv import load_dotenv, find_dotenv, set_key

# Try importing from the newer OpenAI package first
try:
    from openai import OpenAI
    OPENAI_API_VERSION = ">=1.0.0"
except ImportError:
    # Fall back to the older package
    import openai
    OPENAI_API_VERSION = "<1.0.0"

class LLMInterface:
    def __init__(self, api_key=None, api_type=None, base_url=None):
        """Initialize the LLM interface with OpenAI client"""
        # Try to load API key from .env file first
        env_file = find_dotenv()
        if env_file:
            load_dotenv(env_file)
            
        env_api_key = os.getenv("OPENAI_API_KEY")
        env_api_type = os.getenv("API_TYPE")
        env_base_url = os.getenv("BASE_URL")
        
        # Use provided values or fall back to env values
        self.api_key = api_key or env_api_key
        self.api_type = api_type or env_api_type
        self.base_url = base_url or env_base_url
        
        # If still no API key, prompt for credentials
        if not self.api_key:
            self._prompt_for_credentials_and_save()
        else:
            # If we have an API key but no type, detect or prompt
            if not self.api_type:
                self.api_type = self._detect_api_type(self.base_url)
            
            # Set the appropriate model based on API type
            if self.api_type == "gemini":
                self.model = "gemini-2.0-flash"
                if not self.base_url:
                    self.base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
            else:
                # Use different models based on the API version
                if OPENAI_API_VERSION >= "1.0.0":
                    self.model = "gpt-4o-mini"
                else:
                    self.model = "gpt-3.5-turbo"
                
        # Initialize the OpenAI client based on the API version
        if OPENAI_API_VERSION >= "1.0.0":
            # New OpenAI API (>= 1.0.0)
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            # Old OpenAI API (< 1.0.0)
            openai.api_key = self.api_key
            if self.base_url:
                openai.api_base = self.base_url
            self.client = openai
            
        print(f"Using {self.api_type.upper()} API with model: {self.model}")
    
    def _prompt_for_credentials_and_save(self):
        """Prompt the user to select API type and enter credentials, then save to .env file"""
        print("\n=== API Selection ===")
        print("1. OpenAI API")
        print("2. Gemini API")
        
        while True:
            choice = input("Select an option (1 or 2): ")
            if choice in ["1", "2"]:
                break
            print("Invalid choice. Please enter 1 or 2.")
        
        if choice == "1":
            self.api_type = "openai"
            self.model = "gpt-4o-mini"
            self.base_url = None
            print(f"\nYou selected OpenAI API. Using model: {self.model}")
        else:
            self.api_type = "gemini"
            self.model = "gemini-2.0-flash"
            self.base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
            print(f"\nYou selected Gemini API. Using model: {self.model}")
        
        self.api_key = getpass.getpass(f"Enter your {self.api_type.upper()} API key: ")
        
        # Save credentials to .env file
        env_file = find_dotenv()
        if not env_file:
            env_file = os.path.join(os.getcwd(), '.env')
            # Create empty file if it doesn't exist
            if not os.path.exists(env_file):
                with open(env_file, 'w') as f:
                    pass
                
        # Save the values to .env
        set_key(env_file, "OPENAI_API_KEY", self.api_key)
        set_key(env_file, "API_TYPE", self.api_type)
        if self.base_url:
            set_key(env_file, "BASE_URL", self.base_url)
            
        print(f"API credentials saved to {env_file} for future use")
        
    def _detect_api_type(self, base_url):
        """Detect API type based on base URL"""
        if base_url and "generativelanguage.googleapis.com" in base_url:
            return "gemini"
        return "openai"
    
    def generate(self, user_prompt, system_prompt=None, additional_context=None):
        """Generate a response using the LLM"""
        if not system_prompt:
            system_prompt = """You are a terminal-based coding assistant specialized in full-stack development.
            You help users create and modify projects by writing code and explaining concepts.
            Always provide complete, well-structured code that follows best practices.
            When modifying projects, ensure backward compatibility unless otherwise specified.

            When generating JSON responses for file creation or modification, use this schema:
            ```
            [
              {
                "path": "relative/path/to/file.ext",
                "content": "Complete content of the file (never null or undefined)"
              }
            ]
            ```

            Important:
            - The "content" field should never be null or undefined
            - For empty files, use an empty string ("") as content
            - Always include path and content for each file
            - The path should be relative to the project root
            """
        
        messages = [{"role": "system", "content": system_prompt}]
        
        if additional_context:
            messages.append({"role": "system", "content": f"Context information:\n{additional_context}"})
            
        messages.append({"role": "user", "content": user_prompt})
        
        try:
            print("Generating response...")
            
            if OPENAI_API_VERSION >= "1.0.0":
                # New OpenAI API (>= 1.0.0)
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.2,  # Lower temperature for more deterministic outputs
                    max_tokens=8192   # Use a large context window
                )
                return response.choices[0].message.content
            else:
                # Old OpenAI API (< 1.0.0)
                response = self.client.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.2,
                    max_tokens=2048  # Lower limit for older API
                )
                return response['choices'][0]['message']['content']
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return f"Error: {str(e)}"
    
    def extract_json(self, text):
        """Extract JSON from LLM response text"""
        print("Attempting to extract JSON from response...")
        
        # 1. Try to find JSON in code blocks with explicit json language marker
        json_block_pattern = r'```json\s*([\s\S]*?)\s*```'
        json_blocks = re.findall(json_block_pattern, text)
        for block in json_blocks:
            try:
                result = json.loads(block.strip())
                print("Successfully extracted JSON from code block with json marker")
                # Validate file content
                self._validate_file_content(result)
                return result
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON from marked code block: {str(e)}")
                continue
            except Exception as e:
                print(f"Error validating JSON content: {str(e)}")
                continue
        
        # 2. Try to find JSON in any code blocks
        code_block_pattern = r'```\s*([\s\S]*?)\s*```'
        code_blocks = re.findall(code_block_pattern, text)
        for block in code_blocks:
            try:
                result = json.loads(block.strip())
                print("Successfully extracted JSON from general code block")
                # Validate file content
                self._validate_file_content(result)
                return result
            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"Error validating JSON content: {str(e)}")
                continue
        
        # 3. Try to find JSON array or object pattern in the whole text
        json_pattern = r'(\[\s*\{[\s\S]*\}\s*\]|\{\s*"[\s\S]*\})'
        matches = re.findall(json_pattern, text)
        for match in matches:
            try:
                result = json.loads(match.strip())
                print("Successfully extracted JSON using pattern matching")
                # Validate file content
                self._validate_file_content(result)
                return result
            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"Error validating JSON content: {str(e)}")
                continue
        
        # 4. Try to parse the entire text as JSON
        try:
            result = json.loads(text)
            print("Successfully parsed entire text as JSON")
            # Validate file content
            self._validate_file_content(result)
            return result
        except json.JSONDecodeError as e:
            print(f"Failed to parse entire text as JSON: {str(e)}")
        except Exception as e:
            print(f"Error validating JSON content: {str(e)}")
        
        # 5. Try more aggressive cleaning and extraction
        # Remove all markdown syntax, newlines, etc.
        cleaned = re.sub(r'```[\w]*\s*|\s*```', '', text)
        
        # Try to find a JSON array specifically
        array_match = re.search(r'\[\s*\{[\s\S]*?\}\s*\]', cleaned)
        if array_match:
            try:
                result = json.loads(array_match.group(0))
                print("Successfully extracted JSON array after aggressive cleaning")
                # Validate file content
                self._validate_file_content(result)
                return result
            except json.JSONDecodeError as e:
                print(f"Failed to parse extracted array after cleaning: {str(e)}")
            except Exception as e:
                print(f"Error validating JSON content: {str(e)}")
        
        # If we get here, we couldn't find valid JSON
        # Provide info about what we found to help debugging
        print("Could not extract valid JSON from the response")
        
        # Try to extract something that looks like JSON to give a better error message
        json_like = re.search(r'(\[\s*\{[\s\S]{0,100})', text)
        if json_like:
            print(f"Found JSON-like content but couldn't parse it: {json_like.group(0)}...")
        
        raise ValueError("No JSON structure found in response")
    
    def _validate_file_content(self, json_data):
        """Validate and fix file content in JSON data"""
        if not isinstance(json_data, list):
            print("Warning: JSON data is not a list. Cannot validate file content.")
            return
            
        for item in json_data:
            if not isinstance(item, dict):
                continue
                
            if "path" in item and "content" in item and item["content"] is None:
                print(f"Warning: File '{item['path']}' has None content. Setting to empty string.")
                item["content"] = ""
    
    def set_model(self, model_name):
        """Set the LLM model to use"""
        self.model = model_name