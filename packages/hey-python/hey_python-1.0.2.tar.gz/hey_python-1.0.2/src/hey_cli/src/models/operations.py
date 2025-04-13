import os
import subprocess
import shutil
import ultraprint.common as p
from ..utils.display import show_content, show_diff

class OperationRegistry:
    """Registry for operation handlers"""
    _registry = {}
    
    @classmethod
    def register(cls, op_type):
        """Decorator to register an operation class"""
        def decorator(operation_class):
            cls._registry[op_type] = operation_class
            return operation_class
        return decorator
    
    @classmethod
    def get_operation(cls, op_type):
        """Get operation class by type"""
        if (op_type not in cls._registry):
            return None
        return cls._registry[op_type]
    
    @classmethod
    def get_all_operations(cls):
        """Get all registered operations"""
        return cls._registry
    
    @classmethod
    def get_operation_prompt_examples(cls):
        """Get examples of all operations for the system prompt"""
        examples = []
        for op_type, op_class in cls._registry.items():
            if hasattr(op_class, 'get_prompt_example') and op_class.get_prompt_example():
                examples.append(op_class.get_prompt_example())
        return examples

class Operation:
    """Base class for operations"""
    def __init__(self, data):
        self.data = data
        
    def execute(self, cwd):
        """Execute the operation"""
        raise NotImplementedError("Subclasses must implement execute()")
    
    def generate_stream_key(self):
        """Generate a unique key for tracking during streaming"""
        raise NotImplementedError("Subclasses must implement generate_stream_key()")
    
    def display_streaming(self):
        """Display info during streaming"""
        raise NotImplementedError("Subclasses must implement display_streaming()")
    
    @classmethod
    def get_prompt_example(cls):
        """Get an example for the system prompt"""
        return None


@OperationRegistry.register("create_file")
class CreateFile(Operation):
    def execute(self, cwd):
        path = self.data.get("path")
        content = self.data.get("content", "")
        
        if not path:
            p.red("Error: No path specified for create_file operation")
            return
            
        full_path = os.path.join(cwd, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Display file creation message and content without separator
        p.green(f"Created file: {path}")
        p.bold("New file content:")
        show_content(content, is_new=True)
        p.n()  # Add a newline after all content is displayed
    
    def generate_stream_key(self):
        path = self.data.get("path")
        if not path:  # Don't generate a key if path is None/empty
            return None
        return f"create_file:{path}"
    
    def display_streaming(self):
        path = self.data.get("path")
        if not path:  # Skip display if no valid path
            return
        p.green(f"➕ Creating file: {path}")
    
    @classmethod
    def get_prompt_example(cls):
        return {
            "type": "create_file",
            "path": "path/to/file.py",
            "content": "print('Hello, world!')"
        }


@OperationRegistry.register("edit_file")
class EditFile(Operation):
    def execute(self, cwd):
        path = self.data.get("path")
        content = self.data.get("content", "")
        
        if not path:
            p.red("Error: No path specified for edit_file operation")
            return
            
        full_path = os.path.join(cwd, path)
        if not os.path.exists(full_path):
            p.red(f"Cannot edit: File {path} does not exist.")
            return
        
        # Read old content for comparison
        old_content = ""
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                old_content = f.read()
        except:
            p.yellow(f"Warning: Could not read original file content for diff")
        
        # Write new content
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Display without separator
        p.yellow(f"File edited: {path}")
        
        # Show git-style diff between old and new content
        if old_content:
            p.bold("Changes:")
            show_diff(old_content, content)
        p.n()  # Add a newline after all content is displayed
    
    def generate_stream_key(self):
        path = self.data.get("path")
        if not path:
            return None
        return f"edit_file:{path}"
    
    def display_streaming(self):
        path = self.data.get("path")
        if not path:
            return
        p.yellow(f"✏️ Editing file: {path}")
    
    @classmethod
    def get_prompt_example(cls):
        return {
            "type": "edit_file",
            "path": "path/to/existing.py",
            "content": "def new_function():\\n    return 'New code'"
        }


@OperationRegistry.register("delete_file")
class DeleteFile(Operation):
    def execute(self, cwd):
        path = self.data.get("path")
        if not path:
            p.red("Error: No path specified for delete_file operation")
            return
            
        full_path = os.path.join(cwd, path)
        if os.path.exists(full_path):
            # Show file content before deletion without separator
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    p.red(f"Deleted file: {path}")
                    p.bold("Deleted file content:")
                    show_content(content, is_new=False)
            except:
                p.yellow("Could not display file content before deletion")
            
            os.remove(full_path)
            p.n()  # Add a newline after all content is displayed
        else:
            p.red(f"Cannot delete: File {path} does not exist.")
    
    def generate_stream_key(self):
        path = self.data.get("path")
        if not path:
            return None
        return f"delete_file:{path}"
    
    def display_streaming(self):
        path = self.data.get("path")
        if not path:
            return 
        p.red(f"❌ Deleting file: {path}")
    
    @classmethod
    def get_prompt_example(cls):
        return {
            "type": "delete_file",
            "path": "path/to/unwanted_file.txt"
        }


@OperationRegistry.register("rename_file")
class RenameFile(Operation):
    def execute(self, cwd):
        old_path = self.data.get("old_path")
        new_path = self.data.get("new_path")
        
        if not old_path or not new_path:
            p.red("Error: Missing path(s) for rename_file operation")
            return
            
        full_old_path = os.path.join(cwd, old_path)
        full_new_path = os.path.join(cwd, new_path)
        
        if os.path.exists(full_old_path):
            os.makedirs(os.path.dirname(full_new_path), exist_ok=True)
            os.rename(full_old_path, full_new_path)
            p.blue(f"Renamed: {old_path} → {new_path}")
        else:
            p.red(f"Cannot rename: File {old_path} does not exist.")
    
    def generate_stream_key(self):
        old_path = self.data.get("old_path")
        new_path = self.data.get("new_path")
        if not old_path or not new_path:
            return None
        return f"rename_file:{old_path}:{new_path}"
    
    def display_streaming(self):
        old_path = self.data.get("old_path")
        new_path = self.data.get("new_path")
        if not old_path or not new_path:
            return
        p.cyan(f"🔄 Renaming: {old_path} → {new_path}")
    
    @classmethod
    def get_prompt_example(cls):
        return {
            "type": "rename_file",
            "old_path": "path/to/old_name.py",
            "new_path": "path/to/new_name.py"
        }


@OperationRegistry.register("create_directory")
class CreateDirectory(Operation):
    def execute(self, cwd):
        path = self.data.get("path")
        if not path:
            p.red("Error: No path specified for create_directory operation")
            return
            
        full_path = os.path.join(cwd, path)
        os.makedirs(full_path, exist_ok=True)
        p.cyan(f"Created directory: {path}")
    
    def generate_stream_key(self):
        path = self.data.get("path")
        if not path:
            return None
        return f"create_directory:{path}"
    
    def display_streaming(self):
        path = self.data.get("path")
        if not path:
            return
        p.green(f"📁 Creating directory: {path}")
    
    @classmethod
    def get_prompt_example(cls):
        return {
            "type": "create_directory",
            "path": "path/to/new_directory"
        }


@OperationRegistry.register("delete_directory")
class DeleteDirectory(Operation):
    def execute(self, cwd):
        path = self.data.get("path")
        if not path:
            p.red("Error: No path specified for delete_directory operation")
            return
            
        full_path = os.path.join(cwd, path)
        if os.path.exists(full_path) and os.path.isdir(full_path):
            # List files that will be deleted
            files = []
            for root, dirs, filenames in os.walk(full_path):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(file_path, full_path)
                    files.append(rel_path)
            
            p.red(f"Deleted directory: {path}")
            
            if files:
                p.bold("Files being deleted:")
                for file in files[:10]:  # Show only first 10 files
                    p.red(f"  - {file}")
                if len(files) > 10:
                    p.dgray(f"  ... and {len(files) - 10} more files")
            
            shutil.rmtree(full_path)
            p.n()  # Add a newline after all content is displayed
        else:
            p.red(f"Cannot delete: Directory {path} does not exist.")
    
    def generate_stream_key(self):
        path = self.data.get("path")
        if not path:
            return None
        return f"delete_directory:{path}"
    
    def display_streaming(self):
        path = self.data.get("path")
        if not path:
            return
        p.red(f"🧹 Deleting directory: {path}")
    
    @classmethod
    def get_prompt_example(cls):
        return {
            "type": "delete_directory",
            "path": "path/to/unwanted_directory"
        }


@OperationRegistry.register("execute_command")
class ExecuteCommand(Operation):
    def execute(self, cwd):
        command = self.data.get("command")
        if not command:
            p.red("Error: No command specified for execute_command operation")
            return
            
        try:
            p.blue(f"Running: {command}")
            result = subprocess.run(command, shell=True, check=True, text=True, 
                                capture_output=True, cwd=cwd)
            p.green("Command executed successfully")
            if result.stdout.strip():
                p.cyan("Output:")
                for line in result.stdout.splitlines():
                    p.cyan(f"  | {line}")
            p.n()  # Add a newline after all content is displayed
        except subprocess.CalledProcessError as e:
            p.red(f"Command failed: {e}")
            if e.stderr.strip():
                p.purple("Error output:")
                for line in e.stderr.splitlines():
                    p.purple(f"  | {line}")
            p.n()  # Add a newline after all content is displayed
    
    def generate_stream_key(self):
        command = self.data.get("command")
        if not command:
            return None
        return f"execute_command:{command}"
    
    def display_streaming(self):
        command = self.data.get("command")
        if not command:
            return
        p.purple(f"🖥️ Executing: {command}")
    
    @classmethod
    def get_prompt_example(cls):
        return {
            "type": "execute_command",
            "command": "pip install requests"
        }


# Consolidate chat and message types into a single message type
@OperationRegistry.register("message")
class Message(Operation):
    def execute(self, cwd):
        # Messages are handled differently, no execution needed
        pass
    
    def generate_stream_key(self):
        # Messages don't need tracking during streaming
        return None
    
    def display_streaming(self):
        # Message content is displayed through streaming already
        pass
    
    @classmethod
    def get_prompt_example(cls):
        return {
            "type": "message",
            "content": "This is a message to display to the user"
        }


# Register chat as an alias to message for backward compatibility
@OperationRegistry.register("chat")
class Chat(Message):
    """Chat is now an alias for Message for compatibility"""
    @classmethod
    def get_prompt_example(cls):
        # Don't include chat in the examples to discourage its use
        return None
