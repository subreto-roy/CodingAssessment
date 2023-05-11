from django.shortcuts import render


from rest_framework import generics
from .models import Sale
from .serializers import SaleSerializer

class SaleListCreateView(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class SaleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer