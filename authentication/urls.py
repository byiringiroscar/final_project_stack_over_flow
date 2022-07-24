from django.urls import path
from . views import EmailValidationView, UsernameValidationView, PhoneValidationView, page_link_sent, VerificationView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as authViews

urlpatterns = [
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name="validate-email"),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path('validate-phone', csrf_exempt(PhoneValidationView.as_view()), name="validate-phone"),
    path('link_sent/', page_link_sent, name="page_link_sent"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name="activate"),
    path('logout/', authViews.LogoutView.as_view(), {'next_page': 'login'}, name='logout'),
]