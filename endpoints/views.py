from rest_framework import generics, status
from rest_framework.response import Response
from ..main.models import Profile, Referral, Cryptomodel, Portfolio
from .serializers import ProfileSerializer, ReferralSerializer, CryptomodelSerializer, PortfolioSerializer

class ProfileCreateView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ProfileModelView(generics.RetrieveAPIView):
    queryset= Profile.objects.all()
    serializer_class= ProfileSerializer

class CryptomodelCreateView(generics.CreateAPIView):
    queryset = Cryptomodel.objects.all()
    serializer_class = CryptomodelSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CryptomodelDeleteView(generics.DestroyAPIView):
    queryset = Cryptomodel.objects.all()
    serializer_class = CryptomodelSerializer
    lookup_field = 'id_from_API'
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(data= request.data)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReferralListView(generics.ListAPIView):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer

class CryptomodelListView(generics.ListAPIView):
    queryset = Cryptomodel.objects.all()
    serializer_class = CryptomodelSerializer

class CryptomodelDetailView(generics.RetrieveAPIView):
    queryset = Cryptomodel.objects.all()
    serializer_class = CryptomodelSerializer
