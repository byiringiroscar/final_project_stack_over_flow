from django.urls import path
from . import views

urlpatterns = [
    path('', views.super_login, name="super_login"),
    path('logout_super/', views.logout_super, name="logout_super"),

    # ======== work on page ==============================
    path('home_super/', views.home_super, name="home_super"),
    path('stat_skill_admin', views.stat_skill_admin, name='stat_skill_admin'),
    path('all_job_super/', views.all_job_super, name='all_job_super'),
    path('all_job_view_super/<int:id>/', views.all_job_view_super, name='all_job_view_super'),
    path('job_delete_super/<int:id>/', views.job_delete_super, name='job_delete_super'),
    path('applied_job_super/', views.applied_job_super, name='applied_job_super'),
    path('applied_job_profile_super/<int:id>/', views.applied_job_profile_super, name='applied_job_profile_super'),
    path('question_super/', views.question_super, name='question_super'),
    path('delete_question_super/<int:id>/', views.delete_question_super, name='delete_question_super'),
    path('all_user_super/', views.all_user_super, name='all_user_super'),
    path('all_badge_super/', views.all_badge_super, name='all_badge_super'),
    path('invitation_badge_super/<int:id>/', views.invitation_badge_super, name='invitation_badge_super'),
    path('approve_badge/<int:id>/', views.approve_badge, name='approve_badge'),

]
