from export import export_csv


def test_header_and_rows():
    notes = [{"title": "Groceries", "body": "milk"}, {"title": "Ideas", "body": "ship it"}]
    assert export_csv(notes) == "title,body\nGroceries,milk\nIdeas,ship it\n"


def test_empty():
    assert export_csv([]) == "title,body\n"
