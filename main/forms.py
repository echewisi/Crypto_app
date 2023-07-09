from .models import Portfolio, Profile, Referral
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username= forms.ModelForm(required= True, label= 'Username', help_text= "Required. 200 characters or less")
    email= forms.EmailField(required= True, label= "Email", help_text="Required. please enter a valid email", widget= forms.TextInput(attrs={'class': 'form-control'}))
    password1= forms.CharField(required= True, label= 'Password1', help_text="Required. enter valid password", widget= forms.PasswordInput(attrs={'class':'form-control'}))
    password2= forms.CharField(required= True, label='Password2', help_text="Required. enter same password in first placement", widget= forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model= User
        fields=['username', 'email', 'password1', 'password2']