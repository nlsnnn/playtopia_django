from django import forms

from .models import Product


class AddGameForm(forms.ModelForm):
    fields = '__all__'
    exclude = ['reviews']


    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['reviews']
        # fields = []
