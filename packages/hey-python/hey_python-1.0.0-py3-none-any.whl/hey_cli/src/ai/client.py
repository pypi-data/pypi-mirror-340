from openai import OpenAI
from ..config import load_config

def get_response(messages, schema=None):
    config = load_config()
    client = OpenAI(api_key=config["openai_api_key"])
    
    # Create a container to store response data
    response_data = {"text": "", "tokens": 0}
    
    with client.beta.chat.completions.stream(
        model=config["model"],
        messages=messages,
        temperature=config["temperature"],
        response_format=schema
    ) as stream:
        # Attach the stream to the response_data for later access
        response_data["stream"] = stream
        
        for event in stream:
            if event.type == "content.delta":
                chunk = event.delta
                response_data["text"] += chunk
                yield chunk
