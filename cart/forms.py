from django.contrib.auth import get_user_model
from django import forms
from .models import OrderItem, Address


User = get_user_model()


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']


class Addressform(forms.Form):
    "We create our forms fields"
    
    shipping_address_line = forms.CharField(required=False)
    shipping_zip_code = forms.CharField(required=False)
    shipping_city = forms.CharField(required=False)
    shipping_country = forms.CharField(required=False)

    billing_address_line = forms.CharField(required=False)
    billing_zip_code = forms.CharField(required=False)
    billing_city = forms.CharField(required=False)
    billing_country = forms.CharField(required=False)

    "We create our validation form to speed up checkout process"

    selected_shipping_address = forms.ModelChoiceField(
        Address.objects.none(), required=False
    )
    selected_billing_address = forms.ModelChoiceField(
        Address.objects.none(), required=False
    )
    def __init__(self, *args, **kwargs):
        "We are gona filter our users id"
        user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)

        user = User.objects.get(id=user_id)

        "We create a querry filter for address and billing address"
        shipping_address_qs = Address.objects.filter(
            user=user,
            address_type='S'
        )
        billing_address_qs = Address.objects.filter(
            user=user,
            address_type='B'
        )

        self.fields['selected_shipping_address'].queryset = shipping_address_qs
        self.fields['selected_billing_address'].queryset = billing_address_qs
    
    def clean(self):
        data = self.cleaned_data

        "We use our validation selected form for shipping address"
        selected_shipping_address = data.get('selected_shipping_address', None)
        if selected_shipping_address is None:
            if not data.get('shipping_address_line', None):
                self.add_error("shipping_address_line",
                               "Please fill in this field")
            if not data.get('shipping_zip_code', None):
                self.add_error("shipping_zip_code",
                               "Please fill in this field")
            if not data.get('shipping_city', None):
                self.add_error("shipping_city", "Please fill in this field")
            if not data.get('shipping_country', None):
                self.add_error("shipping_country", "Please fill in this field")

        "We use our validation selected form for billing address"
        selected_billing_address = data.get('selected_billing_address', None)
        if selected_billing_address is None:
            if not data.get('billing_address_line', None):
                self.add_error("billing_address_line",
                               "Please fill in this field")
            if not data.get('billing_zip_code', None):
                self.add_error("billing_zip_code",
                               "Please fill in this field")
            if not data.get('billing_city', None):
                self.add_error("billing_city", "Please fill in this field")
            if not data.get('billing_country', None):
                self.add_error("billing_country", "Please fill in this field")