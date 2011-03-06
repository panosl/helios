from django import forms
from django.core.exceptions import ObjectDoesNotExist
from helios.store.models import Category, PaymentOption
from helios.shipping.models import ShippingMethodRegions
from helios.conf import settings
if settings.USE_PAYPAL:
	from helios.paypal.forms import *


class MyCategoryAdminForm(forms.ModelForm):
	class Meta:
		model = Category
	
	def clean_parent(self):
		slug = self.cleaned_data['slug']
		parent = self.cleaned_data['parent']
		if slug and parent:
			try:
				this_category = Category.objects.get(slug = slug)
				parent_category = Category.objects.get(pk = int(parent.id))
				if parent_category.id == this_category.id or parent_category.parent == this_category:
					raise forms.ValidationError('Can\'t have a category as parent of itself.')                
			except ObjectDoesNotExist:
				pass
		return parent


class PaymentForm(forms.Form):
	payment_option = forms.ModelChoiceField(
		queryset = PaymentOption.objects.all(),
		empty_label=None,
		widget=forms.RadioSelect(attrs={
			'class': 'order',
		}),
	)
