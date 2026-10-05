from utils.password import generate_password


def test_password_length():
    password = generate_password(20)

    assert len(password) == 20


def test_password_with_numbers():
    password = generate_password(
        20,
        use_numbers=True,
        use_symbols=False
    )

    assert any(char.isdigit() for char in password)


def test_password_without_numbers():
    password = generate_password(
        20,
        use_numbers=False,
        use_symbols=False
    )

    assert all(char.isalpha() for char in password)