from django import forms
from helios.shipping.models import ShippingMethodRegions


class ShippingChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return u'%s, %s - %s' % (obj.method.name, obj.method.shipper, obj.cost)


class OrderForm(forms.Form):
    def __init__(self, customer, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        methods = [region.shippingmethodregions_set.all()
            for region in customer.country.shippingregion_set.all()]
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
