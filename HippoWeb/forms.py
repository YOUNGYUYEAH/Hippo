from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput
    (attrs={'id': 'username', 'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(label='', widget=forms.PasswordInput
    (attrs={'id': 'password', 'placeholder': 'Password', 'class': 'form-control'}))
