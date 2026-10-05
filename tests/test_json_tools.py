from utils.json_tools import format_json, validate_json


def test_valid_json():
    text = '{"name": "Ahmed", "age": 14}'

    assert validate_json(text) is True


def test_invalid_json():
    text = '{"name": "Ahmed", "age":}'

    assert validate_json(text) is False


def test_format_json():
    text = '{"name":"Ahmed","age":14}'

    result = format_json(text)

    assert '"name": "Ahmed"' in result
    assert '"age": 14' in result