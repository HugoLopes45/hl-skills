NOTES = []


def create_note(title, body):
    note = {"id": len(NOTES) + 1, "title": title, "body": body}
    NOTES.append(note)
    return note
