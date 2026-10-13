from tags import unique_tags


def test_unique_tags_keeps_first_seen_order():
    assert unique_tags(["Beta", "alpha", "beta", "Gamma"]) == ["beta", "alpha", "gamma"]
