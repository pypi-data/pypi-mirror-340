#!/usr/bin/env python3
import sys
import os
import ultraprint.common as p

from .src.core import (
    index_directory, 
    ensure_hey_directory, 
    load_chat_history,
    save_chat_history,
    save_directory_index,
    execute_operations,
    add_user_message,
    add_assistant_message
)
from .src.ai import get_ai_response
from .src.config import Config

def main():
    # Check for special commands first
    if len(sys.argv) > 1:
        # Handle API key removal
        if sys.argv[1] == "--remove-api-key":
            Config.remove_saved_api_key()
            return 0
    
    # Ensure we have the OpenAI API key before proceeding
    Config.get_openai_api_key()
    
    # Skip the program name (sys.argv[0]) and take the rest as the command
    if len(sys.argv) > 1:
        # Join all arguments with spaces to preserve special characters
        message = ' '.join(sys.argv[1:])
    else:
        p.blue("Hi there! How can I help you?")
        return 1
    
    # Get current working directory
    cwd = os.getcwd()
    
    # Setup .hey directory
    hey_dir = ensure_hey_directory(cwd)
    
    # Index directory structure
    dir_index = index_directory(cwd)
    save_directory_index(dir_index, hey_dir)
    
    # Load chat history
    chat_history = load_chat_history(hey_dir)
    
    # Add user message to history
    chat_history = add_user_message(chat_history, message)
    
    # Get AI response with directory index and chat history
    operations = get_ai_response(message, cwd, dir_index, chat_history)
    
    # Add AI response to history
    if operations:
        # Extract message content for normal chat display
        message_contents = []
        for op in operations:
            if op.get("type") in ["chat", "message"]:
                message_contents.append(op.get("content"))
        
        # Add to chat history
        chat_history = add_assistant_message(chat_history, message_contents, operations)
    
    # Save updated chat history
    save_chat_history(chat_history, hey_dir)
    
    # Execute the operations
    execute_operations(operations, cwd)
    
    # Re-index after operations to capture changes
    updated_index = index_directory(cwd)
    save_directory_index(updated_index, hey_dir)
    
    return 0

if __name__ == "__main__":
    main()
