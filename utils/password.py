import secrets
import string


def generate_password(length=12, use_numbers=True, use_symbols=True):
    characters = string.ascii_letters

    if use_numbers:
        characters += string.digits

    if use_symbols:
        characters += string.punctuation

    password = "".join(
        secrets.choice(characters)
        for _ in range(length)
    )

    return password