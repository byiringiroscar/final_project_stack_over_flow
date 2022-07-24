from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_home, name="user_home"),
    path('dashboard_profile/', views.user_dashboard_profile, name="user_dashboard_profile"),
    path('skills_stat', views.skills_stat, name='skills_stat'),
    path('user_create_job/', views.user_create_job, name="user_create_job")
]