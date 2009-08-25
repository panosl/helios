from django import forms
from django.core.exceptions import ObjectDoesNotExist
from helios.store.models import Category, PaymentOption
from helios.shipping.models import ShippingMethodRegions
from helios.conf import settings
if settings.USE_PAYPAL:
	from paypal.standard.forms import PayPalPaymentsForm
	from paypal.standard.widgets import ValueHiddenInput 


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

class ShippingChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return u'%s, %s - %s' % (obj.method.name, obj.method.shipper, obj.cost)

class OrderForm(forms.Form):
	def __init__(self, customer, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		methods = [region.shippingmethodregions_set.all() for region in customer.country.shippingregion_set.all()]
		methods = [method[0] for method in methods]
		self.fields['shipping_choice'].queryset = ShippingMethodRegions.objects.filter(id__in=[method.id for method in methods])

	shipping_choice = ShippingChoiceField(
		queryset=ShippingMethodRegions.objects.all(),
		empty_label=None,
		widget=forms.RadioSelect(attrs={
			'class': 'order',
			'onclick': '$("#shipping_choice").submit()',
		})
	)

class PaymentForm(forms.Form):
	payment_option = forms.ModelChoiceField(
		queryset = PaymentOption.objects.all(),
		empty_label=None,
		widget=forms.RadioSelect(attrs={
			'class': 'order',
		}),
	)

if settings.USE_PAYPAL:
	class MyPayPalForm(PayPalPaymentsForm):
		first_name = forms.CharField(widget=ValueHiddenInput())
		last_name = forms.CharField(widget=ValueHiddenInput())
		address_override = forms.IntegerField(widget=ValueHiddenInput(), initial=0)
