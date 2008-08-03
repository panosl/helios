# Helios, a Phaethon-Designs, e-commerce software.
# Copyright (C) 2008 Panos Laganakos <panos.laganakos@gmail.com>

import unittest
from django.test.client import Client
from django.test import TestCase


customer_data = {
	'username': 'panosl',
	'first_name': 'Panos',
	'last_name': 'Laganakos',
	'email': 'panos.laganakos@gmail.com',
	'address': 'omirou 17',
	'country': '1',
	'password1': '12345',
	'password2': '12345',
}

class CustomerCreationTest(unittest.TestCase):
	def setUp(self):
		self.client = Client()

	def test_creation(self):
		response = self.client.post('/customer/', customer_data)

		self.failUnlessEqual(response.status_code, 200)

		print response.context[0]
