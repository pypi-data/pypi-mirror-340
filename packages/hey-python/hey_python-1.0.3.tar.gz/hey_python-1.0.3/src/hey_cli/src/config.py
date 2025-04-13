import os
import json
import dotenv
import keyring
import getpass
import ultraprint.common as p
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib
import platform

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
    
    # Fallback file storage settings
    FALLBACK_DIR = os.path.join(os.path.expanduser("~"), ".hey_config")
    FALLBACK_FILE = os.path.join(FALLBACK_DIR, "credentials.enc")
    
    @classmethod
    def _get_machine_key(cls):
        """Generate a stable machine-specific key for encryption"""
        # Create a machine-specific but stable identifier
        machine_id = f"{platform.node()}:{platform.machine()}:{os.getuid() if hasattr(os, 'getuid') else os.getlogin()}"
        # Hash it to get a stable byte sequence
        digest = hashlib.sha256(machine_id.encode()).digest()
        # Convert to a key usable by Fernet
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            salt=b'hey_cli_salt_v1',  # Fixed salt
            iterations=100000,
            length=32
        )
        key = base64.urlsafe_b64encode(kdf.derive(digest))
        return key
        
    @classmethod
    def _save_to_fallback(cls, api_key):
        """Save API key to fallback encrypted file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(cls.FALLBACK_DIR, mode=0o700, exist_ok=True)
            
            # Encrypt the API key
            key = cls._get_machine_key()
            fernet = Fernet(key)
            encrypted_key = fernet.encrypt(api_key.encode())
            
            # Save to file with restricted permissions
            with open(cls.FALLBACK_FILE, 'wb') as f:
                f.write(encrypted_key)
            
            # Set restrictive permissions
            os.chmod(cls.FALLBACK_FILE, 0o600)
            return True
        except Exception as e:
            p.red(f"Error saving API key to fallback storage: {str(e)}")
            return False
    
    @classmethod
    def _load_from_fallback(cls):
        """Load API key from fallback encrypted file"""
        try:
            if not os.path.exists(cls.FALLBACK_FILE):
                return None
                
            # Read and decrypt the API key
            with open(cls.FALLBACK_FILE, 'rb') as f:
                encrypted_key = f.read()
                
            key = cls._get_machine_key()
            fernet = Fernet(key)
            api_key = fernet.decrypt(encrypted_key).decode()
            return api_key
        except InvalidToken:
            p.yellow("Stored API key appears to be corrupted or was encrypted on a different machine.")
            return None
        except Exception:
            # Don't print debug messages for fallback storage attempts
            return None
    
    @classmethod
    def _delete_from_fallback(cls):
        """Delete API key from fallback storage"""
        try:
            if os.path.exists(cls.FALLBACK_FILE):
                os.remove(cls.FALLBACK_FILE)
                return True
            return False
        except Exception as e:
            p.red(f"Error removing API key from fallback storage: {str(e)}")
            return False

    @classmethod
    def get_openai_api_key(cls):
        """Get OpenAI API key from environment or keyring, prompt if not found"""
        # First check environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            # Try to get from keyring with fallback to file storage
            try:
                api_key = keyring.get_password(cls.KEYRING_SERVICE, cls.KEYRING_USERNAME)
            except Exception:
                # Don't print debug messages for keyring errors unless we need to prompt
                # Try fallback storage
                api_key = cls._load_from_fallback()
            
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
                try:
                    # First try to save to system keyring
                    keyring.set_password(cls.KEYRING_SERVICE, cls.KEYRING_USERNAME, api_key)
                    p.green("✓ API key saved in system keyring.")
                except Exception:
                    # Fall back to file storage without showing keyring error
                    if cls._save_to_fallback(api_key):
                        p.green("✓ API key saved to fallback encrypted storage.")
                    else:
                        p.red("Could not save API key. It will need to be entered again next time.")
        
        cls.OPENAI_API_KEY = api_key
        return api_key
    
    @classmethod
    def remove_saved_api_key(cls):
        """Remove the API key from keyring storage and fallback storage"""
        keyring_removed = False
        fallback_removed = False
        
        # Try to remove from keyring
        try:
            existing_key = keyring.get_password(cls.KEYRING_SERVICE, cls.KEYRING_USERNAME)
            if existing_key:
                keyring.delete_password(cls.KEYRING_SERVICE, cls.KEYRING_USERNAME)
                p.green("✓ API key has been removed from system keyring.")
                keyring_removed = True
        except Exception:
            # Don't show keyring errors, just continue to fallback
            pass
        
        # Also try to remove from fallback storage
        if cls._delete_from_fallback():
            p.green("✓ API key has been removed from fallback storage.")
            fallback_removed = True
            
        if not keyring_removed and not fallback_removed:
            p.yellow("No saved API keys were found.")
            return False
            
        return True

def load_config():
    """Load configuration"""
    # Ensure we have the API key
    openai_api_key = Config.get_openai_api_key()
    
    return {
        "openai_api_key": openai_api_key,
        "model": Config.MODEL,
        "temperature": Config.TEMPERATURE
    }
