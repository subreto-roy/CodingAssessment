from django.urls import path
from reports.views import generate_report

urlpatterns = [
    # Other URL patterns
    path('generate-report/', generate_report, name='generate_report'),
]
