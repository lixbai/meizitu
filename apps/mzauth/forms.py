from django import forms
from apps.forms_errors import FormErrorMixin

class LoginForm(forms.Form, FormErrorMixin):
    email = forms.CharField(max_length=100)
    password = forms.CharField(min_length=6, max_length=16)
    remember = forms.IntegerField(required=False)

