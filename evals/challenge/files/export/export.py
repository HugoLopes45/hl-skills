def export_csv(notes):
    lines = ["title,body"]
    for note in notes:
        lines.append(f"{note['title']},{note['body']}")
    return "\n".join(lines) + "\n"
