from ..main.models import Cryptomodel, Referral, Profile, Portfolio
from rest_framework import serializers

class CryptomodelSerializer(serializers.ModelSerializer):
    class Meta:
        model= Cryptomodel
        fields= "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields= "__all__"
        
class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model= Referral
        fields= "__all__"

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model= Portfolio
        fields= "__all__"