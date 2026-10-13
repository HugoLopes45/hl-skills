from shop.cart import Cart


def checkout(prices):
    cart = Cart()
    for price in prices:
        cart.add(price)
    return {"total": cart.total()}
