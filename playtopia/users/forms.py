from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True)

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'first_name', 'last_name']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
