from django.contrib import admin
from .models import Profile, Referral, Cryptomodel, Portfolio

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=[
        'user',
        'referral_code',
        'bonus'
    ]
    
@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display= [
        'user',
        'referrer',
    ]

@admin.register(Cryptomodel)
class CryptoAdmin(admin.ModelAdmin):
    list_display=[
        'user',
        'name',
        'id_from_API',
        'symbol',
    ]

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display=[
        'user',
        'total_value'
    ]
    



# Register your models here.
