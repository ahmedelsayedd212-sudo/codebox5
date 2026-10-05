def count_words(text):
    words = text.split()
    return len(words)


def count_characters(text):
    return len(text)


def reverse_text(text):
    return text[::-1]


def remove_extra_spaces(text):
    return " ".join(text.split())


def to_uppercase(text):
    return text.upper()


def to_lowercase(text):
    return text.lower()