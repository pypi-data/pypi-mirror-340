import json
import re
from pydantic import BaseModel

def extract_json_content(content):
    """Extract valid JSON from a string that might contain JSON or Pydantic model"""
    if isinstance(content, BaseModel):
        return content.model_dump(by_alias=True)

    if isinstance(content, dict):
        return content
    
    try:
        # Check for JSON in code block
        pattern = r'```json(.*?)```'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return json.loads(match.group(1).strip())
        else:
            return json.loads(content)
    except Exception as e:
        return content

def extract_readable_content(json_string):
    """Extract readable content from a partial JSON string"""
    result = {}
    
    # Try to find operation type
    type_match = re.search(r'"type"\s*:\s*"([^"]+)"', json_string)
    if type_match:
        result["type"] = type_match.group(1)
    
    # Try to find content
    content_match = re.search(r'"content"\s*:\s*"((?:[^"\\]|\\.)*?)(?:"|$)', json_string, re.DOTALL)
    if content_match:
        content = content_match.group(1)
        result["content"] = content
    
    # Try to find path - use a simpler pattern that works with any path format
    path_match = re.search(r'"path"\s*:\s*"([^"]*)"', json_string)
    if path_match:
        result["path"] = path_match.group(1)
    
    # Try to find command - also use a simpler pattern
    command_match = re.search(r'"command"\s*:\s*"([^"]*)"', json_string)
    if command_match:
        result["command"] = command_match.group(1)
    
    return result

def replace_escape_sequences(text):
    """
    Replace JSON-style escape sequences with their actual characters.
    This handles cases where we're extracting content from a partially parsed JSON string.
    """
    replacements = [
        ('\\n', '\n'),    # newline
        ('\\t', '\t'),    # tab
        ('\\r', '\r'),    # carriage return
        ('\\"', '"'),     # double quote
        ('\\\'', "'"),    # single quote
        ('\\\\', '\\'),   # backslash
        ('\\b', '\b'),    # backspace
        ('\\f', '\f'),    # form feed
        ('\\v', '\v'),    # vertical tab
        ('\\a', '\a')     # bell
    ]
    
    for pattern, replacement in replacements:
        text = text.replace(pattern, replacement)
    
    return text
