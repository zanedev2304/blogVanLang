from django.urls import path,include
from .views import home_view,profile_view


urlpatterns = [
    path('',home_view,name='home_view'),
    path('profile/',profile_view,name='profile'),
]
