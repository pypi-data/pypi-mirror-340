import os
import json
import dotenv
import keyring
import getpass
import ultraprint.common as p

# Load environment variables from .env file if it exists
dotenv.load_dotenv()

class Config:
    # AI configuration
    OPENAI_API_KEY = None
    # Hardcoded model and temperature values
    MODEL = "gpt-4o"
    TEMPERATURE = 0.5
    
    # File and directory settings
    HEY_DIRECTORY = ".hey"
    MAX_FILE_SIZE = 1024 * 1024  # 1MB
    
    # File types to read content from
    CODE_EXTENSIONS = [
        '.py', '.js', '.html', '.css', '.json', '.md', '.txt', '.ini', '.yml', '.yaml',
        '.xml', '.c', '.cpp', '.h', '.java', '.go', '.rs', '.sh', '.bat', '.ps1', 
        '.ts', '.jsx', '.tsx', '.rb', '.php'
    ]
    
    # Folders to ignore when indexing
    IGNORE_FOLDERS = [
        '.hey', 'node_modules', '__pycache__', '.git', '.idea', '.vscode', 
        'venv', 'dist', 'build', 'bin', 'obj', 'target',
        'packages', 'bower_components', 'jspm_packages', 'vendor', '.next', 
        '.nuxt', '.output', '.cache', '.parcel-cache', '.pnp'
    ]
    
    # Display settings
    MAX_DIFF_LINES = 50
    MAX_CONTENT_LINES = 20
    CONTEXT_LINES = 1

    # Keyring service name for storing the API key
    KEYRING_SERVICE = "hey_cli"
    KEYRING_USERNAME = "openai_api_key"

    @classmethod
    def get_openai_api_key(cls):
        """Get OpenAI API key from environment or keyring, prompt if not found"""
        # First check environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            # Try to get from keyring
            api_key = keyring.get_password(cls.KEYRING_SERVICE, cls.KEYRING_USERNAME)
            
        if not api_key:
            # If still not found, prompt the user
            p.yellow("OpenAI API key not found. Please enter your API key:")
            api_key = getpass.getpass("API Key: ")
            
            # Validate the API key format (basic check)
            if not api_key.startswith("sk-") or len(api_key) < 20:
                p.red("The API key format looks incorrect. It should start with 'sk-' and be longer.")
                retry = input("Do you want to try again? (y/n): ")
                if retry.lower() == 'y':
                    return cls.get_openai_api_key()
                else:
                    p.red("Cannot continue without a valid API key.")
                    import sys
                    sys.exit(1)
            
            # Ask if they want to save it
            save = input("Would you like to save this API key securely? (y/n): ")
            if save.lower() == 'y':
                keyring.set_password(cls.KEYRING_SERVICE, cls.KEYRING_USERNAME, api_key)
                p.green("API key saved securely. It won't ask again on this machine.")
        
        cls.OPENAI_API_KEY = api_key
        return api_key
    
    @classmethod
    def remove_saved_api_key(cls):
        """Remove the API key from keyring storage"""
        try:
            # Check if a key exists before attempting to delete
            existing_key = keyring.get_password(cls.KEYRING_SERVICE, cls.KEYRING_USERNAME)
            
            if existing_key:
                keyring.delete_password(cls.KEYRING_SERVICE, cls.KEYRING_USERNAME)
                p.green("✓ API key has been removed from secure storage.")
                return True
            else:
                p.yellow("No saved API key found in secure storage.")
                return False
        except Exception as e:
            p.red(f"Error removing API key: {str(e)}")
            return False

def load_config():
    """Load configuration"""
    # Ensure we have the API key
    openai_api_key = Config.get_openai_api_key()
    
    return {
        "openai_api_key": openai_api_key,
        "model": Config.MODEL,
        "temperature": Config.TEMPERATURE
    }
