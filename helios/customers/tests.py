# -*- coding: utf-8 -*-
'''
    customers.tests
    ~~~~~~~~~~~~~~~

    :copyright: 2007-2008 by Panos Laganakos.
'''

#import unittest
#from django.test.client import Client
from django.test import TestCase


customer_data = {
	'username': 'panosl',
	'first_name': 'Panos',
	'last_name': 'Laganakos',
	'email': 'panos.laganakos@gmail.com',
	'address': 'omirou 17',
	'city': 'Kalamata',
	'country': '1',
	'password1': '12345',
	'password2': '12345',
}

class CustomerCreationTest(TestCase):
	fixtures = ['countries.yaml']

	def test_view(self):
		response = self.client.get('/customer/register/')
		self.failUnlessEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'customer.html')

	def test_creation(self):
		response = self.client.post('/customer/register/', customer_data)
		self.assertRedirects(response, '/', status_code=302, target_status_code=301)
