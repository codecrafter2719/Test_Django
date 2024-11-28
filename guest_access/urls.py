from django.urls import path,include
from . import views

urlpatterns = [
    # path('',views.about,name='about'),
    path('', views.home, name='home'),


    # path('', views.home, name='home'),
   
]

