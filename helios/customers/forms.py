# -*- coding: utf-8 -*-
'''
    customers.forms
    ~~~~~~~~~~~~~~~

    :copyright: 2007-2008 by Panos Laganakos.
'''
from django import forms
#from django.core.validators import alnum_re
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from helios.customers.models import Country


class CustomerForm(forms.Form):
	username = forms.RegexField(regex=r'^\w+$', max_length=30,
		label=_('Username'))
	first_name = forms.CharField(label=_('First name'), max_length=30)
	last_name = forms.CharField(label=_('Last name'), max_length=30)
	email = forms.EmailField(label=_('Email'))
	address = forms.CharField(label=_('Address'), max_length=50)
	city = forms.CharField(max_length=30)
	# zip_postal
	country = forms.ModelChoiceField(queryset=Country.objects.all())
	password1 = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)

	def clean_username(self):
		#if not alnum_re.search(self.cleaned_data['username']):
			#raise forms.ValidationError([_('Usernames can only contain letters, numbers and underscores')])
		try:
			user = User.objects.get(username__exact=self.cleaned_data['username'])
		except User.DoesNotExist:
			return self.cleaned_data['username']
		raise forms.ValidationError([_('This username is already taken, please choose another.')])

	def clean_email(self):
		try:
			user = User.objects.get(email__exact=self.cleaned_data['email'])
		except User.DoesNotExist:
			return self.cleaned_data['email']
		raise forms.ValidationError([_('This email is already being used, please use another.')])

	def clean_password1(self):
		'''Check length of the password.'''
		pwd1 = self.cleaned_data.get('password1', None)
		if pwd1 and len(pwd1) < 4:
			raise forms.ValidationError([_('Your password is too short \
				(4 characters at least)')])
		else:
			return self.cleaned_data['password1']

	def clean_password2(self):
		'''Check that the same password is entered twice'''
		if self.cleaned_data.get('password1', None):
			if self.cleaned_data.get('password2', None) and \
				self.cleaned_data['password1'] == \
				self.cleaned_data['password2']:
				return self.cleaned_data['password2']
			else:
				raise forms.ValidationError([_('You should entered the same password \
					twice')])
		else:
			if self.cleaned_data.get('password2', None):
				raise forms.ValidationError([_('You should entered the same password \
					twice')])
			else:
				return self.cleaned_data['password2']

class CreateCustomerForm(CustomerForm):
	pass
