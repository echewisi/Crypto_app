import shortuuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile

#a referral code will be generated here for each user
def create_referral_code():
    return shortuuid.ShortUUID().random(length=10)

@receiver(post_save, sender= User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile= Profile.objects.create(user= instance, referral_code= create_referral_code())
        profile.save()
    