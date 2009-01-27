CART_TESTS = """
>>> from helios.store.cart import Cart, CartLine

>>> c = Cart()
>>> c.add_product(product_id=1, quantity=20)
>>> c[1]
{'id': 1, 'quantity': 20}
>>> #c[1].price

"""

# vi:ft=python
