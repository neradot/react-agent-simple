import json

def parse_json(str):
    str_json = str.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(str_json)
    except json.decoder.JSONDecodeError:
        raise ValueError(f"Invalid JSON: {str}")