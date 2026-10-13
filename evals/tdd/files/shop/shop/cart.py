class Cart:
    def __init__(self):
        self._items = []

    def add(self, price):
        self._items.append(price)

    def total(self):
        return sum(self._items)
