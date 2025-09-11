from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'state', 'zipcode']
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your delivery address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'State'
            }),
            'zipcode': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'ZIP Code'
            }),
        }