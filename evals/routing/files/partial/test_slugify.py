from slugify import slugify


def test_lowercase_and_dashes():
    assert slugify("Hello World") == "hello-world"
