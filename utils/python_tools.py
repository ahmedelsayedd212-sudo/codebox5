import keyword


def count_lines(code):
    """Count non-empty lines of Python code."""
    return sum(
        1
        for line in code.splitlines()
        if line.strip()
    )


def count_functions(code):
    """Count Python function definitions."""
    return sum(
        1
        for line in code.splitlines()
        if line.strip().startswith("def ")
    )


def count_classes(code):
    """Count Python class definitions."""
    return sum(
        1
        for line in code.splitlines()
        if line.strip().startswith("class ")
    )


def find_imports(code):
    """Find import statements."""
    imports = []

    for line in code.splitlines():
        stripped = line.strip()

        if stripped.startswith("import "):
            imports.append(stripped)

        elif stripped.startswith("from "):
            imports.append(stripped)

    return imports


def check_keywords(text):
    """Find Python keywords inside text."""
    words = text.split()

    return [
        word
        for word in words
        if word in keyword.kwlist
    ]