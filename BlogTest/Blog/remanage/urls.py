from django.urls import path,include
from .views import case_detail,case_list,create_case,update_case,home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('caselist/', case_list, name='case_list'),
    path('create/', create_case, name='create_case'),
    path('<int:id>/', case_detail, name='case_detail'),
    path('<int:id>/update/', update_case, name='update_case'),
]
