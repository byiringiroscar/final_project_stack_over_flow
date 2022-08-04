from django.urls import path
from . import views

urlpatterns = [
    path('', views.super_login, name="super_login"),
    path('home_super/', views.home_super, name="home_super")
]
