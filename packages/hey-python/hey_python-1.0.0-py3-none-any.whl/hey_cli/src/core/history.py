import os
import json
import time

def ensure_hey_directory(cwd):
    """Create .hey directory if it doesn't exist"""
    hey_dir = os.path.join(cwd, '.hey')
    if not os.path.exists(hey_dir):
        os.makedirs(hey_dir)
    return hey_dir

def load_chat_history(hey_dir):
    """Load chat history from .hey/chat_history.json"""
    history_path = os.path.join(hey_dir, 'chat_history.json')
    if os.path.exists(history_path):
        with open(history_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_chat_history(chat_history, hey_dir):
    """Save chat history to .hey/chat_history.json"""
    history_path = os.path.join(hey_dir, 'chat_history.json')
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(chat_history, f, indent=2)

def save_directory_index(index, hey_dir):
    """Save directory index to .hey/directory_index.json"""
    index_path = os.path.join(hey_dir, 'directory_index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)
    return index_path

def add_user_message(chat_history, message):
    """Add a user message to the chat history"""
    chat_history.append({
        "role": "user", 
        "content": message, 
        "timestamp": time.time()
    })
    return chat_history

def add_assistant_message(chat_history, message_contents, operations):
    """Add an assistant message to the chat history"""
    combined_message = "\n\n".join(message_contents) if message_contents else "No message provided."
    
    chat_history.append({
        "role": "assistant", 
        "content": combined_message,
        "timestamp": time.time(),
        "operations": operations  # Store the complete operations list
    })
    return chat_history
