from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_home, name="user_home"),
    path('dashboard_profile/', views.user_dashboard_profile, name="user_dashboard_profile"),
    path('skills_stat', views.skills_stat, name='skills_stat'),
    path('user_create_job/', views.user_create_job, name="user_create_job"),
    path('job_user_admin/', views.job_user_admin, name="job_user_admin"),
    path('delete_job_user_admin/<int:id>/', views.delete_job_user_admin, name="delete_job_user_admin"),
    path('job_user_view_admin/<int:id>/', views.job_user_view_admin, name="job_user_view_admin"),
    path('job_person_applied_all/<int:id>/', views.job_person_applied_all, name="job_person_applied_all"),
    path('job_applied_admin/', views.job_applied_admin, name="job_applied_admin"),
    path('applied_profile/<int:id>/', views.applied_profile, name="applied_profile"),
    path('invitation_applied/<int:id>/', views.invitation_applied, name="invitation_applied"),
    path('hire_person_admin/<int:id>/', views.hire_person_admin, name="hire_person_admin"),
    path('question_admin/', views.question_admin, name="question_admin"),
    path('edit_question_admin/<int:id>/', views.edit_question_admin, name="edit_question_admin"),
    path('request_badger_user/', views.request_badger_user, name="request_badger_user"),
]