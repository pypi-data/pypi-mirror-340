import os
import platform
import time
import datetime
from ..config import Config
import ultraprint.common as p  # Import ultraprint

def index_directory(cwd):
    """Index the current directory structure including file contents"""
    # Print that indexing is happening
    p.dgray("🔎 Analyzing Files")
    
    index = {
        "files": [],
        "directories": [],
        "file_contents": {},
        "system_info": get_system_info()  # Add system information
    }
    
    for root, dirs, files in os.walk(cwd):
        # Filter out directories we want to ignore
        dirs[:] = [d for d in dirs if d not in Config.IGNORE_FOLDERS]
        
        # Add relative paths
        rel_root = os.path.relpath(root, cwd)
        if rel_root != '.':
            index["directories"].append(rel_root)
            
        for file in files:
            rel_path = os.path.join(rel_root, file) if rel_root != '.' else file
            index["files"].append(rel_path)
            
            # Read file content if it's a recognized code file
            full_path = os.path.join(root, file)
            _, ext = os.path.splitext(file)
            
            if ext.lower() in Config.CODE_EXTENSIONS:
                try:
                    # Check file size before reading
                    file_size = os.path.getsize(full_path)
                    if file_size <= Config.MAX_FILE_SIZE:
                        with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                            content = f.read()
                            index["file_contents"][rel_path] = content
                    else:
                        # For large files, store a note instead of content
                        index["file_contents"][rel_path] = f"[File too large to index: {file_size} bytes]"
                except Exception as e:
                    # If file can't be read, store the error
                    index["file_contents"][rel_path] = f"[Error reading file: {str(e)}]"
    
    # Clear the "Indexing directory..." line after indexing is complete
    p.cls_prev()
    
    return index

def format_directory_context(dir_index):
    """Format directory index into readable context for the AI"""
    # Format the file structure
    files_list = "\n".join(dir_index.get('files', []))
    dirs_list = "\n".join(dir_index.get('directories', []))
    
    # Add system information to the context
    system_info = dir_index.get('system_info', {})
    system_info_str = "\n".join([f"{k}: {v}" for k, v in system_info.items()]) if system_info else "Not available"
    
    directory_context = f"""
System Information:
{system_info_str}

Current directory structure:
Files: 
{files_list}

Directories:
{dirs_list}

Current workspace files:
"""
    
    # Add file contents with clear separators
    file_contents = dir_index.get('file_contents', {})
    for filepath, content in file_contents.items():
        # Add file contents with markdown code block formatting
        file_ext = os.path.splitext(filepath)[1].lstrip('.')
        if not file_ext:
            file_ext = 'txt'
            
        directory_context += f"\n\n--- File: {filepath} ---\n```{file_ext}\n{content}\n```"
    
    return directory_context

def get_system_info():
    """Gather system information like time, date, OS, etc."""
    now = datetime.datetime.now()
    
    return {
        "current_time": now.strftime("%H:%M:%S"),
        "current_date": now.strftime("%Y-%m-%d"),
        "day_of_week": now.strftime("%A"),
        "timestamp": time.time(),
        "operating_system": platform.system(),
        "os_release": platform.release(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "current_directory": os.getcwd()
    }
