import posts


def test_post_url():
    assert posts.post_url("Hello World") == "/posts/hello-world"
