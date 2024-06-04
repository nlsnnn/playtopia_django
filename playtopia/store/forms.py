from django import forms

from .models import Product, Review


class AddGameForm(forms.ModelForm):
    fields = '__all__'
    exclude = ['reviews']


    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['reviews']
        # fields = []


class AddReviewForm(forms.ModelForm):
    rating = forms.IntegerField(max_value=5, min_value=1)
    fields = ['text', 'rating']

    class Meta:
        model = Review
        fields = ['text', 'rating']
