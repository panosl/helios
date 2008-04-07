# Helios, a Phaethon-Designs, e-commerce software.
# Copyright (C) 2008 Panos Laganakos <panos.laganakos@gmail.com>

#TODO when we move up from 0.96.1, change form.clean_data to form.cleaned_data

from django import newforms as forms
from django.core.validators import alnum_re
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from customers.models import Country


class CustomerForm(forms.Form):
	username = forms.CharField(label=_('Username'), max_length=30)
	first_name = forms.CharField(label=_('First name'), max_length=30)
	last_name = forms.CharField(label=_('Last name'), max_length=30)
	email = forms.EmailField()
	address = forms.CharField(max_length=50)
	city = forms.CharField(max_length=30)
	# zip_postal
	country = forms.ModelChoiceField(queryset=Country.objects.all())
	password1 = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)

	def clean_username(self):
		if not alnum_re.search(self.clean_data['username']):
			raise forms.ValidationError([_('Usernames can only contain letters, numbers and underscores')])
		try:
			user = User.objects.get(username__exact=self.clean_data['username'])
		except User.DoesNotExist:
			return self.clean_data['username']
		raise forms.ValidationError([_('This username is already taken, please choose another.')])

	def clean_email(self):
		try:
			user = User.objects.get(email__exact=self.clean_data['email'])
		except User.DoesNotExist:
			return self.clean_data['email']
		raise forms.ValidationError([_('This email is already being used, please use another.')])

	def clean_password1(self):
		'''Check length of the password.'''
		pwd1 = self.clean_data.get('password1', None)
		if pwd1 and len(pwd1) < 4:
			raise forms.ValidationError([_('Your password is too short \
				(4 characters at least)')])
		else:
			return self.clean_data['password1']

	def clean_password2(self):
		'''Check that the same password is entered twice'''
		if self.clean_data.get('password1', None):
			if self.clean_data.get('password2', None) and \
				self.clean_data['password1'] == \
				self.clean_data['password2']:
				return self.clean_data['password2']
			else:
				raise forms.ValidationError([_('You should entered the same password \
					twice')])
		else:
			if self.clean_data.get('password2', None):
				raise forms.ValidationError([_('You should entered the same password \
					twice')])
			else:
				return self.clean_data['password2']

class CreateCustomerForm(CustomerForm):
	pass
