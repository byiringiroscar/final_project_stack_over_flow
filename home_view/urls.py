from django.urls import path
from . import views
from authentication.views import login_user, register_user

urlpatterns = [
    path('', views.home, name="home"),
    path('question/', views.question, name="question"),
    path('question_detail/<int:id>/', views.question_detail, name="question_detail"),
    path('ask_question/', views.ask_question, name="ask_question"),
    path('job_list/', views.job_list, name="job_list"),
    path('job_detail/<int:id>/', views.job_detail, name="job_detail"),
    path('login/', login_user, name="login"),
    path('register/', register_user, name="register"),
    path('setting/', views.user_profile, name="user_profile"),
    path('skills/', views.skills_update, name="skills_update"),
    path('view_profile/', views.view_profile, name="view_profile"),
    path('view_profile_outside/<int:id>/', views.view_profile_outside, name="view_profile_outside"),
    path('notifications/', views.notifications, name="notifications"),
]