from django import forms
from django.core.exceptions import ValidationError
from todo.models import CustomUser


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Your username'}))
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs={'placeholder': 'Your email address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}), min_length=4)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username):
            raise ValidationError('This username is already used')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email):
            raise ValidationError('This email address is already used')
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your email address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}))


class TaskForm(forms.Form):
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'I write my task'}))
