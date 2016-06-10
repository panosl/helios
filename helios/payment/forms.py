from django import forms

from helios.payment.models import PaymentOption


class PaymentForm(forms.Form):
    payment_option = forms.ModelChoiceField(
        queryset=PaymentOption.objects.all(),
        empty_label=None,
        widget=forms.RadioSelect(attrs={
            'class': 'order',
        }),
    )
