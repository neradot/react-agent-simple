import json
import openai

def parse_json(str):
    str_json = str.replace("<reasoning>", "").replace("</reasoning>", "").strip()
    try:
        return json.loads(str_json)
    except json.decoder.JSONDecodeError:
        raise ValueError(f"Invalid JSON: {str}")

def get_completion(messages, model, **kwargs) -> openai.types.completion.Completion:
    openai_client = openai.OpenAI()
    response = openai_client.chat.completions.create(messages=messages, model=model, **kwargs)
    return response
