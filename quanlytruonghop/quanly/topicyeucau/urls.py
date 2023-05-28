from django.urls import path,include
from .views import home_view,create_request,login_view,logout_view,update_user_profile,my_topic_detail,mytopic,ArticleDetailView,manage_view,manage_request,rate_topic,KnowledgeDetailView,article_update_view,article_delete_view ,article_hide_view,article_unhide_view
from .views import create_article,article_list,create_knowledge,knowledge_list
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.conf.urls.static import static
from . import views 

urlpatterns = [

    path('microsoft_authentication/callback', views.microsoft_callback, name='microsoft_callback'),
    path('',home_view,name='home'),
 
    path('signin', views.sign_in, name='signin'),
    path('signout', views.sign_out, name='signout'),
    path('callback', views.callback, name='callback'),





    path('create_request/',create_request,name='create_request'),
    path('account/my-topic/', mytopic, name='my-topic'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    
    path('update_profile/', update_user_profile, name='account_profile'),
    path('topic/<int:id>/', my_topic_detail, name='topic_detail'),
    path('create_acticle/', create_article, name='create_article'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article_list/', article_list, name='article_list'),
    path('article/<int:pk>/update/', article_update_view, name='article_update_view'),
    path('article/<int:pk>/delete/', article_delete_view, name='article_delete_view'),
    path('article/<int:pk>/hide/', article_hide_view, name='article_hide_view'),
    path('article/<int:pk>/unhide/', article_unhide_view, name='article_unhide_view'),
    
    path('knowledge/<int:pk>/', KnowledgeDetailView.as_view(), name='knowledge_detail'),
    path('create_knowledge/', create_knowledge, name='create_knowledge'),
    path('knowledge_list/', knowledge_list, name='knowledge_list'),
    



    path('manage/',manage_view,name='manage_view'),
    path('manage_request/',manage_request,name='manage_request'),
    path('rate/',rate_topic,name='rate-view'),



    

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)