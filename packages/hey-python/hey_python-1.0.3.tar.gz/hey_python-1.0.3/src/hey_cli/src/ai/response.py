import json
import ultraprint.common as p
from ..utils.parsing import extract_readable_content, replace_escape_sequences
from ..core.indexer import format_directory_context
from .client import get_response
from .prompts import get_system_prompt
from ..models.schema import OpsList
from ..models.operations import OperationRegistry

def get_ai_response(user_message, cwd, dir_index=None, chat_history=None):
    """Get response from AI based on user message"""
    
    system_prompt = get_system_prompt(cwd)
    
    # Convert chat history to proper format if provided
    messages = []
    
    # Add chat history if provided (excluding the current message)
    if (chat_history):
        for msg in chat_history[:-1]:  # Skip the last message as we'll add it separately
            # Only include user and assistant messages, skip system messages
            if msg.get("role") in ["user", "assistant"]:
                # For assistant messages, check if we have operations data
                if msg.get("role") == "assistant" and "operations" in msg:
                    # Include both the message content and a JSON representation of operations
                    op_json = json.dumps(msg.get("operations"), indent=2)
                    enhanced_content = f"{msg.get('content')}\n\nPrevious operations:\n```json\n{op_json}\n```"
                    messages.append({"role": msg.get("role"), "content": enhanced_content})
                else:
                    messages.append({"role": msg.get("role"), "content": msg.get("content")})
    
    # Add directory index as a system message if provided
    if dir_index:
        directory_context = format_directory_context(dir_index)
        messages.append({"role": "system", "content": directory_context})

    messages.append({"role": "system", "content": system_prompt})

    # Add the current user message
    messages.append({"role": "user", "content": user_message})
    
    try:        
        stream = get_response(messages, schema=OpsList)
        
        # Process the streaming response and display operations in real time
        operations = stream_json_operations(stream)

        if not operations:
            p.red("No valid operations found in response")
            return [{"type": "message", "content": f"Response received but couldn't be processed properly."}]
        
        # Convert any "chat" operations to "message" for consistency
        for op in operations:
            if op.get("type") == "chat":
                op["type"] = "message"
                
        return operations
    except Exception as e:
        p.red(f"Error communicating with AI: {e}")
        import traceback
        traceback.print_exc()
        return [{"type": "message", "content": f"Error communicating with AI: {e}"}]

def stream_json_operations(stream):
    buffer = ""
    in_object = False
    found_ops_key = False
    ops_array_started = False
    current_object = None
    brace_depth = 0
    bracket_depth = 0
    operations = []
    last_displayed_content = ""
    stream_display_active = False
    update_counter = 0
    # Track which operations we've already announced
    announced_operations = set()
    
    for chunk in stream:
        buffer += chunk
        
        # Continue processing until we can't extract more complete objects
        while buffer:
            if not buffer:
                break
            
            # Start of the main object that contains "ops" key
            if not in_object and buffer and buffer[0] == '{':
                in_object = True
                brace_depth = 1
                buffer = buffer[1:]
                continue
            
            # Look for "ops" key if we're in the main object but haven't found the key yet
            if in_object and not found_ops_key and '"ops"' in buffer:
                pos = buffer.find('"ops"')
                # Skip to the colon after "ops"
                colon_pos = buffer.find(':', pos)
                if (colon_pos > -1):
                    buffer = buffer[colon_pos+1:].lstrip()
                    found_ops_key = True
                    continue
            
            # Look for start of array after finding "ops" key
            if found_ops_key and not ops_array_started and buffer and buffer[0] == '[':
                ops_array_started = True
                bracket_depth = 1
                buffer = buffer[1:].lstrip()
                continue
            
            # Process array items
            if ops_array_started:
                # Start of an operation object
                if buffer and buffer[0] == '{' and current_object is None:
                    current_object = '{'
                    brace_depth = 1
                    buffer = buffer[1:]
                    continue
                
                # If we're currently building an object
                if current_object is not None:
                    # Scan through buffer adding to current object
                    i = 0
                    while i < len(buffer):
                        char = buffer[i]
                        current_object += char
                        
                        if char == '{':
                            brace_depth += 1
                        elif char == '}':
                            brace_depth -= 1
                            # Object complete
                            if brace_depth == 0:
                                # Process the complete object
                                try:
                                    obj = json.loads(current_object)
                                    # Clear any partial content display before showing complete message
                                    if stream_display_active:
                                        # Add a newline after streamed message content
                                        p.n()
                                        stream_display_active = False
                                    
                                    # Before adding to operations, check if it's a delete_file or other operation
                                    # that hasn't been announced yet for streaming display
                                    op_type = obj.get("type")
                                    if op_type and op_type != "message" and op_type != "chat":
                                        # Generate a stream key for this complete operation
                                        operation_class = OperationRegistry.get_operation(op_type)
                                        if operation_class:
                                            operation = operation_class(obj)
                                            stream_key = operation.generate_stream_key()
                                            
                                            # Display if not already announced
                                            if stream_key and stream_key not in announced_operations:
                                                operation.display_streaming()
                                                announced_operations.add(stream_key)
                                    
                                    operations.append(obj)
                                except json.JSONDecodeError:
                                    pass
                                
                                # Reset for next object
                                current_object = None
                                buffer = buffer[i+1:].lstrip()
                                break
                        
                        i += 1
                        
                    # If we processed the whole buffer but object isn't complete
                    if current_object and brace_depth > 0:
                        # Try to display partial content during streaming
                        update_counter += 1
                        if update_counter % 1 == 0:  # Only check periodically to improve performance
                            try:
                                partial_info = extract_readable_content(current_object)
                                if "type" in partial_info:
                                    # Normalize chat type to message for consistency
                                    if partial_info["type"] == "chat":
                                        partial_info["type"] = "message"
                                        
                                    # Get the operation handler from the registry
                                    op_type = partial_info["type"]
                                    operation_class = OperationRegistry.get_operation(op_type)
                                    
                                    # Handle message type operations specially for content streaming
                                    if op_type == "message" and "content" in partial_info:
                                        # Display streaming content as it comes in
                                        new_content = partial_info["content"]
                                        # Only display the newly added content
                                        if new_content != last_displayed_content:
                                            added_content = new_content[len(last_displayed_content):]
                                            if added_content:  # Only print if there's something new
                                                added_content = replace_escape_sequences(added_content)
                                                p.blue(added_content, end='', flush=True)
                                            last_displayed_content = new_content
                                            stream_display_active = True
                                    # For other operation types, use their display_streaming method
                                    elif operation_class:
                                        # Create operation instance and get its stream key
                                        operation = operation_class(partial_info)
                                        stream_key = operation.generate_stream_key()
                                        
                                        # Only display once per unique operation
                                        if stream_key and stream_key not in announced_operations:
                                            operation.display_streaming()
                                            announced_operations.add(stream_key)
                            except Exception as e:
                                p.dgray(f"DEBUG: Exception in streaming: {e}", flush=True)
                                import traceback
                                p.dgray(traceback.format_exc(), flush=True)

                        buffer = ""
                        break
                
                # Handle comma between objects or end of array
                if current_object is None and buffer:
                    if buffer[0] == ',':
                        buffer = buffer[1:].lstrip()
                        continue
                    elif buffer[0] == ']':
                        # End of ops array
                        bracket_depth -= 1
                        ops_array_started = False
                        buffer = buffer[1:]
                        continue
            
            # If we've gone through everything and can't process more, wait for next chunk
            if buffer and (not in_object or (in_object and not found_ops_key) or 
                        (found_ops_key and not ops_array_started)):
                break
            
            # If we can't make progress with the current buffer, wait for more data
            if not buffer:
                break
    
    # Add a final newline if we were streaming message content
    if stream_display_active:
        p.n()
        stream_display_active = False
    
    # Convert any chat operations to message for consistency
    for op in operations:
        if op.get("type") == "chat":
            op["type"] = "message"
    
    return operations
