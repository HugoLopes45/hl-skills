import json


def count_words(text):
    count = 0
    for _ in text.split():
        # increment the counter
        count += 1
    return count
