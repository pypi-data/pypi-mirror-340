import os
import subprocess
import shutil
import ultraprint.common as p
from ..utils.display import show_content, show_diff
from ..models.operations import OperationRegistry

def execute_operations(operations, cwd):
    """Execute the operations returned by the AI"""
    # Safety check - ensure operations is iterable
    if operations is None:
        p.red("Warning: No operations to execute")
        return
    
    #delete ["message", "chat"] operations from the list
    operations = [op for op in operations if op.get("type") not in ["message", "chat"]]

    if operations:
        p.dgray("-" * 50)  # Add a visual separator line

    for op in operations:
        op_type = op.get("type")
        
        # Get the operation handler from the registry
        operation_class = OperationRegistry.get_operation(op_type)
        
        if operation_class:
            # Create an instance and execute it
            operation = operation_class(op)
            operation.execute(cwd)
        else:
            p.dgray(f"Unknown operation type: {op_type}")
            p.n()

def create_file(path, content, cwd):
    """Create a file with given content"""
    full_path = os.path.join(cwd, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    p.green(f"Created file: {path}")
    # Show the new content with line numbers and highlight as added content
    p.bold("\nNew file content:")
    show_content(content, is_new=True)

def edit_file(path, content, cwd):
    """Edit a file with given content"""
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
    
    p.yellow(f"File edited: {path}")
    
    # Show git-style diff between old and new content
    if old_content:
        p.bold("\nChanges:")
        show_diff(old_content, content)

def delete_file(path, cwd):
    """Delete a file"""
    full_path = os.path.join(cwd, path)
    if os.path.exists(full_path):
        # Show file content before deletion
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                p.bold("\nDeleted file content:")
                show_content(content, is_new=False)  # Show as deleted content
        except:
            p.yellow("Could not display file content before deletion")
        
        os.remove(full_path)
        p.red(f"Deleted file: {path}")
    else:
        p.red(f"Cannot delete: File {path} does not exist.")

def rename_file(old_path, new_path, cwd):
    """Rename a file"""
    full_old_path = os.path.join(cwd, old_path)
    full_new_path = os.path.join(cwd, new_path)
    
    if os.path.exists(full_old_path):
        os.makedirs(os.path.dirname(full_new_path), exist_ok=True)
        os.rename(full_old_path, full_new_path)
        p.blue(f"Renamed: {old_path} → {new_path}")
    else:
        p.red(f"Cannot rename: File {old_path} does not exist.")

def create_directory(path, cwd):
    """Create a directory"""
    full_path = os.path.join(cwd, path)
    os.makedirs(full_path, exist_ok=True)
    p.cyan(f"Created directory: {path}")

def delete_directory(path, cwd):
    """Delete a directory"""
    full_path = os.path.join(cwd, path)
    if os.path.exists(full_path) and os.path.isdir(full_path):
        # List files that will be deleted
        files = []
        for root, dirs, filenames in os.walk(full_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, full_path)
                files.append(rel_path)
        
        if files:
            p.bold("\nFiles being deleted:")
            for file in files[:10]:  # Show only first 10 files
                p.red(f"  - {file}")
            if len(files) > 10:
                p.dgray(f"  ... and {len(files)} more files")  # Fixed from len.files to len(files)
        
        shutil.rmtree(full_path)
        p.red(f"Deleted directory: {path}")
    else:
        p.red(f"Cannot delete: Directory {path} does not exist.")

def execute_command(command, cwd):
    """Execute a shell command"""
    try:
        p.blue(f"Running: {command}")
        
        # For Windows systems, ensure we don't get stuck on pause commands in batch files
        if os.name == 'nt' and command.endswith('.bat'):
            # Execute with /C option to avoid getting stuck on pause
            process = subprocess.Popen(f'cmd /C {command}', 
                                    shell=True, 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE,
                                    text=True,
                                    cwd=cwd)
        else:
            process = subprocess.Popen(command,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True,
                                    cwd=cwd)
        
        # Print output in real-time
        p.cyan("Output:")
        stdout_data = ""
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                line = output.strip()
                p.cyan(f"  | {line}")
                stdout_data += output
        
        # Get the return code
        return_code = process.poll()
        
        # Check for errors
        if return_code != 0:
            stderr = process.stderr.read()
            p.red(f"Command failed with return code {return_code}")
            if stderr.strip():
                p.purple("Error output:")
                for line in stderr.splitlines():
                    p.purple(f"  | {line}")
        else:
            p.green("Command executed successfully")
            
    except Exception as e:
        p.red(f"Command execution error: {e}")
        import traceback
        p.red(traceback.format_exc())
