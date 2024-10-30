import json
import openai

def parse_json(str):
    str_json = str.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(str_json)
    except json.decoder.JSONDecodeError:
        raise ValueError(f"Invalid JSON: {str}")

def get_completion(messages) -> str:
    openai_client = openai.OpenAI()
    model = "gpt-4o"
    response = openai_client.chat.completions.create(messages=messages, model=model)
    return response.choices[0].message.content
