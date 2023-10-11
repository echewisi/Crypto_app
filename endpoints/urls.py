from django.urls import path, include
from .views import CryptomodelCreateView, CryptomodelDeleteView, CryptomodelDetailView, CryptomodelListView, ReferralListView, ProfileCreateView, ProfileModelView
from rest_framework.routers import DefaultRouter

router= DefaultRouter()
router.register(r'profiles', ProfileCreateView)
router.register(r'cryptomodels', CryptomodelCreateView)

urlpatterns = [
    path('api/', include(router.urls)), 
    path('api/cryptomodels/<str:id_from_API>/', CryptomodelDeleteView.as_view(), name='cryptomodel-delete'),    
    path('api/referrals/', ReferralListView.as_view(), name='referral-list'),
    path('api/cryptomodels/', CryptomodelListView.as_view(), name='cryptomodel-list'),
    path('api/cryptomodels/<str:id_from_API>/', CryptomodelDetailView.as_view(), name='cryptomodel-detail'),
]
