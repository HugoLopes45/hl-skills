from notes import create_note


def test_create_note():
    assert create_note("Groceries", "milk")["title"] == "Groceries"
