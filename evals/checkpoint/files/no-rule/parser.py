def parse_line(line):
    key, value = line.split("=")
    return key.strip(), value.strip()
