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
    

class Cryptomodel(models.Model):
    #name here is also the the ID of the crytptocurrentcy. it is useful for API calls
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name= "cryptocurrencies", null= True)
    id_from_API= models.CharField(max_length=20)
    name= models.CharField(max_length= 20)
    symbol= models.CharField(max_length= 10)
    current_price= models.DecimalField(max_digits=10, decimal_places=2)
    quantity= models.DecimalField(max_digits= 10, decimal_places=2, default=1)
    
    class Meta:
        unique_together= ('user', 'name')
        
    def __str__(self)-> str:
        return f'{self.user.username}'

#we create a portfolio linked to a user and store total value of the portfolio/stats
class Portfolio(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE, related_name="portfolios")
    total_value= models.DecimalField(max_digits= 15, decimal_places=2)
    
    def __str__(self)-> str:
        return f'{self.user.username + "has a value of:" + self.total_value}'

# Create your models here.
