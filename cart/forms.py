from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(0, 6)]

class CartAddForm(forms.Form):
    cart_quantity = forms.TypedChoiceField(choices = PRODUCT_QUANTITY_CHOICES, coerce=int, initial=1, label="Количество")
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
class CartAddOneForm(forms.Form):
    cart_quantity = forms.TypedChoiceField(initial=1, coerce=int, widget=forms.HiddenInput)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
    