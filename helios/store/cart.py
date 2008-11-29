from helios.store.models import Product

class Cart(dict):
	"""
	A dict-like object, which stores ``Product.id``:``CartLine`` pairs, in the form of:
	{ID: {'id': ID, 'quantity': QUANTITY}}

	Examples:

	>>> cart = Cart()
	>>> cart.add_product(id=1, quantity=20)
	"""

	def __init__(self, **products):
		super(Cart, self).__init__(products)

	def add_product(self, product_id, quantity=1):
		"""
		Add product to ``Cart``.

		If product already in ``Cart`` add to the quantity.
		"""
		if self.has_key(product_id):
			self[product_id]['quantity'] += quantity
		else:
			self[product_id] = CartLine(id=product_id, quantity=quantity)

	def remove_product(self, product_id):
		del self[product_id]

	def get_product_list(self):
		"""
		Return the product_list based on the currently stored IDs.
		"""
		product_list = Product.objects.in_bulk(self.keys())
		return product_list.values()

	def get_product_count(self):
		return sum((product['quantity'] for product in self.itervalues()))

	def get_price(self):
		"""
		Sum and return the price of each ``CartLine``.
		"""
		#return sum((cart_line.get_price() for cart_line in self.itervalues()), Decimal('0.00'))
		return sum((cart_line.get_price() for cart_line in self.itervalues()))

class CartLine(dict):
	def __init__(self, **line):
		super(CartLine, self).__init__(line)
	
	def get_product(self):
		product = Product.objects.get(id__exact=self['id'])
		return product

	def get_quantity(self):
		return self['quantity']

	def set_quantity(self, quantity):
		self['quantity'] = quantity

	def get_price(self):
		price = self.get_product().price * self['quantity']
		#return Decimal(str(price))
		return price
