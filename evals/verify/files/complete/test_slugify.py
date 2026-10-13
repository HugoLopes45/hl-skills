from slugify import slugify


def test_lowercase_and_dashes():
    assert slugify("Hello World") == "hello-world"


def test_collapses_whitespace():
    assert slugify("  a   b ") == "a-b"
