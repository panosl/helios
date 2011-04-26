from django import forms
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.widgets import ValueHiddenInput


class MyPayPalForm(PayPalPaymentsForm):
	first_name = forms.CharField(widget=ValueHiddenInput())
	last_name = forms.CharField(widget=ValueHiddenInput())
	address_override = forms.IntegerField(widget=ValueHiddenInput(),
		initial=0)
