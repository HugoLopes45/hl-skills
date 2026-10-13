def page(items, number, size):
    start = number * size
    return items[start:start + size - 1]
