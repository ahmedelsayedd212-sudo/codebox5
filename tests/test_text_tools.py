from utils.text_tools import (
    count_words,
    count_characters,
    reverse_text,
    remove_extra_spaces,
    to_uppercase,
    to_lowercase
)


def test_count_words():
    assert count_words("Hello Ahmed") == 2


def test_count_characters():
    assert count_characters("Ahmed") == 5


def test_reverse_text():
    assert reverse_text("Ahmed") == "demhA"


def test_remove_extra_spaces():
    assert remove_extra_spaces("Hello     Ahmed") == "Hello Ahmed"


def test_uppercase():
    assert to_uppercase("hello") == "HELLO"


def test_lowercase():
    assert to_lowercase("HELLO") == "hello"