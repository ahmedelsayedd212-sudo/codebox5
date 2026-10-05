from utils.python_tools import (
    count_lines,
    count_functions,
    count_classes,
    find_imports,
    check_keywords
)


def test_count_lines():

    code = """
print("Hello")

print("Ahmed")
"""

    assert count_lines(code) == 2


def test_count_functions():

    code = """
def hello():
    pass

def test():
    pass
"""

    assert count_functions(code) == 2


def test_count_classes():

    code = """
class User:
    pass

class Admin:
    pass
"""

    assert count_classes(code) == 2


def test_find_imports():

    code = """
import os
from math import sqrt
"""

    result = find_imports(code)

    assert len(result) == 2


def test_keywords():

    result = check_keywords(
        "def hello return if else"
    )

    assert "def" in result
    assert "return" in result
    assert "if" in result