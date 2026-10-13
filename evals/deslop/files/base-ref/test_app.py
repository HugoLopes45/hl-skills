from app import count_words


def test_count_words():
    assert count_words("a b  c") == 3


def test_slugify():
    from app import slugify

    assert slugify("Hello, World!") == "hello-world"
