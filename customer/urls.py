from django.urls import path , include
from customer import views 
from .views import *



urlpatterns = [
    path('country/',views.countryV),
    path('city/',views.cityV),
    path('city/<slug>/',views.cityV),
    path('address/',views.addressV)
]