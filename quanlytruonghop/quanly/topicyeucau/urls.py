from django.urls import path,include
from .views import home_view,create_request




urlpatterns = [
    path('',home_view,name='home'),
    path('create_request/',create_request,name='create_request'),
]