from django.urls import path,include
from .views import home_view,create_request,login_view,logout_view,update_user_profile,my_topic_detail,mytopic,ArticleDetailView,manage_view,manage_request
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('microsoft_authentication/home',home_view,name='home'),
    path('',home_view,name='home'),
    path('create_request/',create_request,name='create_request'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    
    path('update_profile/', update_user_profile, name='account_profile'),
    path('topic/<int:id>/', my_topic_detail, name='topic_detail'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('account/my-topic/', mytopic, name='my-topic'),
    path('manage/',manage_view,name='manage_view'),
    path('manage_request/',manage_request,name='manage_request')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)