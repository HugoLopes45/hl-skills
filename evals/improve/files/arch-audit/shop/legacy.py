def export_xml(rows):
    out = ["<rows>"]
    for row in rows:
        out.append(f"<row name='{row['name']}' total='{row['total']}'/>")
    out.append("</rows>")
    return "\n".join(out)
