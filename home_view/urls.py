from django.urls import path
from . import views
from authentication.views import login_user, register_user
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

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
    path('connect_with_me/<int:id>/', views.connect_with_me, name="connect_with_me"),
    # get the notification data
    path('get_notification', views.get_notification, name="get_notification"),
    path('mark_read_notif', csrf_exempt(views.mark_read_notif), name="mark_read_notif"),
    path('get_all_Notification_count', csrf_exempt(views.get_all_Notification_count), name="get_all_Notification_count"),
    # api for change to enable two-factor authentication
    path('enable-2-authentication', csrf_exempt(views.enable_two_factor), name="enable_two_factor"),

    # reset password and recovery it
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='reset_password'), # here also we are going to customise our own template
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete'),

]