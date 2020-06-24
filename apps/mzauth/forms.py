from django import forms
from apps.forms_errors import FormErrorMixin

class LoginForm(forms.Form, FormErrorMixin):
    email = forms.CharField(max_length=100)
    password = forms.CharField(min_length=6, max_length=20, error_messages={'min_length':'密码要超过6位', 'max_length':'密码最多20位'})
    remember = forms.IntegerField(required=False)

