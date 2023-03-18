from django.shortcuts import render,HttpResponse
from django.template import loader

# Create your views here.


def home_view(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def profile_view(request):
    template = loader.get_template('account/profile.html')
    return HttpResponse(template.render())