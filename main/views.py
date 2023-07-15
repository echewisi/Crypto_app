import requests
from django.shortcuts import render, redirect
from .models import Referral, Portfolio, Profile, Cryptomodel
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from  django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template.defaultfilters import slugify
from django.utils.http import urlsafe_base64_decode
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("portfolio")
    if request.method== "POST":
        form= CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user= form.save(commit= False)
            user.password= make_password(form.cleaned_data['password1'])
            user.email= form.cleaned_data['email']
            user.save()
            messages.success(request, "you have signed up!", extra_tags="success!")
            return redirect('login')
    
    else:
        form= CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

#if user is already logged in:
def refer_view(request, referral_code):
    if request.user.is_authenticated:
        return redirect('portfolio')
    try:
        #get the user profile of the referrer
        referrer= User.objects.get(profile__referral_code= referral_code)
    except User.DoesNotExist:
        #show error message if the referrer does not exist
        return HttpResponse('Referrer does not exist')
    
    if request.method== 'POST':
        form= UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.password= make_password(form.cleaned_data['password1'])
            user.email=form.cleaned_data['email']
            user.save()
            #create a referral instance
            referral= Referral.objects.create(user=user,  referrer= referrer)
            referral.save()
            
            if referrer is not None:
                referrer.profile.bonus += 100  #add referral bonus to referrer
                referrer.profile.save()
                messages.success(request, f'{referrer.username} received a bonus of 100 points. you signed up with their referral link ')
            messages.success(request, "you have successfully signed up!")
            return redirect('login')
    else:
        form= CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})


# Create your views here.1
