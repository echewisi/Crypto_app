from django.urls import path
from .views import CryptomodelCreateView, CryptomodelDeleteView, CryptomodelDetailView, CryptomodelListView, ReferralListView, ProfileCreateView, ProfileModelView
from rest_framework.routers import DefaultRouter

# router= DefaultRouter()
# router.register(r'profiles', ProfileCreateView)
# router.register(r'cryptomodels', CryptomodelCreateView)

urlpatterns = [
    path('register/', ProfileCreateView.as_view(), name= 'profile-create'), 
    path('profile_user/<int:pk>', ProfileModelView.as_view(), name='profile_view'),
    path('cryptomodels/<str:id_from_API>/', CryptomodelDeleteView.as_view(), name='cryptomodel-delete'),    
    path('referrals/', ReferralListView.as_view(), name='referral-list'),
    path('cryptomodels/', CryptomodelListView.as_view(), name='cryptomodel-list'),
    path('cryptomodel_detail/<str:id_from_API>/', CryptomodelDetailView.as_view(), name='cryptomodel-detail'),
]
