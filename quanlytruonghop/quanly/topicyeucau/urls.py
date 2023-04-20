from django.urls import path,include
from .views import home_view,create_request,login_view,logout_view,AccountView,update_user_profile,TopicDetailView,mytopic,ArticleDetailView,manage_view,manage_request
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('',home_view,name='home'),
    path('create_request/',create_request,name='create_request'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('account/', AccountView.as_view(), name='account-view'),
    path('account/update_profile/', update_user_profile, name='update_profile'),
    path('topic/<int:pk>/', TopicDetailView.as_view(), name='topic_detail'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('account/my-topic/', mytopic, name='my-topic'),
    path('manage/',manage_view,name='manage_view'),
    path('manage_request/',manage_request,name='manage_request')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)