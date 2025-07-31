from django import forms
from .models import Maker

class BrandFilterForm(forms.Form):
    brand = forms.ModelMultipleChoiceField(
        queryset = Maker.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple
    )