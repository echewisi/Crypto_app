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

def onboarding_view(request):
    
    return render(request,'onboarding.html')

def home_view(request):
    topten_crypto_url="https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=10&page=1&sparkline=true"
    topten_crypto_data= requests.get(topten_crypto_url).json()
    #if user is logged in:
    if request.user.is_authenticated:
        user_Cryptocurrencies= Cryptomodel.objects.filter(user= request.user)
        user_portfolio= Portfolio.objects.filer(user= request.user).first()
        #checks the prices for the user's cryptocurrencies:
        names= [crypto.name for crypto in user_Cryptocurrencies]
        symbols= [crypto.symbol for crypto in user_Cryptocurrencies]
        ids=[crypto.id_from_Api for crypto in user_Cryptocurrencies]
        prices=[]
        
        #this shows tge price change of user's cryptocurrencies in the last 24 hours and not the percentage change to reduce the number of API calls(only 10-20 per minute are allowed for free users)
        for crypto_id in ids:
            prices_url= f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd&include_24hr_change=true'
            prices_data= requests.get(prices_url).json()
            price_change= prices_data[crypto_id]['usd_24h_change']
            prices.append(price_change)
        
        #a dictionary for names and prices    
        crypto_prices_changes= dict(zip(names, prices))    
        
        context={
            'topten_crypto_data': topten_crypto_data,
            'user_Cryptocurrencies': user_Cryptocurrencies,
            'user_porftfolio': user_portfolio,
            'crypto_price_changes': crypto_prices_changes
        }
    else:
        context= {'topten_crypto_data': topten_crypto_data}
    return render(request, 'home.html', context)


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


def login_view(request):
    if request.user.is_authenticated:
        return redirect('portfolio')
    
    if request.method == "POST":
        form= AuthenticationForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data.get('username')
            raw_password= form.cleaned_data.get('password')
            user= authenticate(request, username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('portfolio')
        else:
            messages.error(request, 'invalid username or password', extra_tags='warning')
    else:
        form= AuthenticationForm()
    return render(request, 'login.html', {'form':form})


@login_required(login_url= 'login')
def logout_view(request):
    logout(request)
    messages.success(request, 'you have successfully logged out!')
    return redirect('home')



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

@login_required(login_url='login')
def search_view(request):
    if request.method != 'POST':
        #this will throw a 405 error if the request method iss not POST
        return HttpResponseNotAllowed(['POST'], "only post requests are allowed. return to search")
    if not (search_query:=request.POST.get('search_query')):
        return HttpResponse('No cryptocurrency found based on your search!')

    api_url= f'https://api.coingecko.com/api/v3/search?query={search_query}'
    response= requests.get(api_url)
    search_results= response.json()
    try:
        data= search_results['coins']
    except IndexError:
        return HttpResponse('no crypto currency found based on your search')
    
    coin_id= data['id']
    image= data['large']
    symbol= data['symbol']
    market_cap= data['market_cap_rank']
    
    #check if the crypto currency is already in the user's portfolio and pass that information to the template
    current_user= request.user
    is_already_in_portfolio= False
    
    user_cryptocurrencies= Cryptomodel.objects.filter(user= request.user)
    for cryptocurrency in user_cryptocurrencies:
        if cryptocurrency.name.lower()== coin_id.lower():
            is_already_in_portfolio= True
    
    context={
        'data': data,
        'coin_id': coin_id,
        'image': image,
        'symbol': symbol,
        'market_cap': market_cap,
        'is_already_in_portfolio': is_already_in_portfolio
    }
    
    return render(request, 'search.html', context)
# Create your views here.
