from django import forms

class UserLoginForm(forms.Form):
    Username = forms.CharField(label="")
    Password = forms.CharField(label="",widget=forms.PasswordInput)