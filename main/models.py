from django.db import models
from django.contrib.auth.models import User

#this method is to override the default user model to make the email unique
User._meta.get_field('email')._unique= True

class Profile(models.Model):
    user= models.OneToOneField(User, on_delete= models.CASCADE)
    referral_code= models.CharField(max_length=5 , unique= True)
    bonus= models.IntegerField(default= 0)
    
    def __str__(self) -> str:
        return self.user.username
    

class Referral(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    referrer= models.ForeignKey(User, on_delete= models.CASCADE, related_name='refer_person')
    
    def __str__(self)-> str:
        return f'{"user:" + self.user.username + "was referred by:" + self.referrer.username}'

# Create your models here.
