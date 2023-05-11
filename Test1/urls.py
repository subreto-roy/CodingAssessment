from django.contrib import admin
from django.urls import path

from accounts.views import RegistrationAPIView, LoginAPIView
from sales.views import SaleListCreateView, SaleRetrieveUpdateDestroyView
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegistrationAPIView.as_view(), name='register'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/sales/', SaleListCreateView.as_view(), name='sale-list-create'),
    path('api/sales/<int:pk>/', SaleRetrieveUpdateDestroyView.as_view(), name='sale-retrieve-update-destroy'),
    path('reports/', include('reports.urls')),
]

