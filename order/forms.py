from django import forms

QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 4)]


class AddToCartForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES,
                                      coerce=int)
