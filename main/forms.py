from django import forms

from main.models import Destination, DestinationImage


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'description', 'price', 'category']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('Price must be more than Zero')
        return price


class DestinationImageForm(forms.ModelForm):
    class Meta:
        model = DestinationImage
        fields = ['image']