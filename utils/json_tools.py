import json


def format_json(text):
    data = json.loads(text)

    return json.dumps(
        data,
        indent=4,
        ensure_ascii=False
    )


def validate_json(text):
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False