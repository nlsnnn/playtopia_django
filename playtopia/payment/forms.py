from django import forms
from django.contrib.auth import get_user_model


class CheckoutForm(forms.ModelForm):
    # email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['email']
