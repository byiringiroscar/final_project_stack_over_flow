from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
import json
from validate_email import validate_email
from django.contrib.auth import get_user_model
import phonenumbers
from authentication.forms import UserForm
from django.contrib import messages
from django.utils.encoding import force_str, DjangoUnicodeDecodeError, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from authentication.utils import account_activation_token
from django.core.mail import EmailMessage
import threading
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

User = get_user_model()


# Create your views here.
# make email threading for sent email
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def login_user(request):
    user_on = request.user
    if user_on.is_authenticated:
        return redirect('home')
    form = AuthenticationForm()
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                if user.is_verified:
                    login(request, user)
                    return redirect('home')
                elif not user.is_verified:
                    messages.info(request, "your account is not verified please check inbox link to verify it")
                    return redirect('login')
            else:
                messages.error(request, "invalid credential try again")
                return redirect('login')
        else:
            messages.error(request, "all fields are required")
            return redirect('login')
    return render(request, 'login_user.html')


def logout_user(request):
    user = request.user
    logout(user)
    return redirect('login')


def register_user(request):
    user_on = request.user
    if user_on.is_authenticated:
        return redirect('home')
    email = request.POST.get('email')
    full_name = request.POST.get('full_name')
    phone_number = request.POST.get('phone_number')
    password = request.POST.get('password')
    password_2 = request.POST.get('password_2')
    user_check = User.objects.filter(email=email, is_verified=False)
    form = UserForm()
    if user_check:
        messages.info(request, "this user already exist please verify account")
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            form.save()
            user = User.objects.get(email=email, phone_number=phone_number)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('activate',
                           kwargs={'uidb64': uidb64, 'token': account_activation_token.make_token(user)})
            activate_url = 'http://' + domain + link
            print("activation url =======================", activate_url)
            email_subject = "Activate your account"
            email_body = f"Hi {user.full_name} please use this link to verify your account\n {activate_url}"
            email = EmailMessage(
                email_subject,
                email_body,
                'from@example.com',
                [email],
            )
            EmailThread(email).start()
            messages.success(request, "account created successfully please verify it")
            return redirect('page_link_sent')
    else:
        form = UserForm()
    context = {
        'form': form,
        'fieldValues': request.POST
    }

    return render(request, 'register_user.html', context)


def page_link_sent(request):
    return render(request, 'page_link_sent.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if not account_activation_token.check_token(user, token):
                messages.info(request, "User already activated")
                return redirect('login', messages=messages)
            if user.is_verified:
                return redirect('login')
            user.is_verified = True
            user.save()
            messages.success(request, "Account activated successfully")
            return redirect('login')
        except Exception as ex:
            pass
        return redirect('login')


# login ================ phase =======================


# =============== validation fields ==============

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': "Email is invalid"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': "sorry email is taken"}, status=409)
        return JsonResponse({'email_valid': True})


class PhoneValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        phone_number = data['phone_number']

        if not phone_number.startswith('+'):
            return JsonResponse({"phone_error": "phone number must start with plus(+)"})
        if User.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({'phone_error': "sorry phone number taken"})
        try:
            phone_valid_check = phonenumbers.parse(phone_number)
            if not phonenumbers.is_possible_number(phone_valid_check):
                return JsonResponse({"phone_error": "phone number is invalid"})
        except:
            return JsonResponse({"phone_error": "phone number is invalid"})
        return JsonResponse({"phone_valid": True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': "username should only contain alphanumeric character"}, status=400)
        if len(username) < 4:
            return JsonResponse({'username_error': "Username is small"}, status=400)
        return JsonResponse({'username_valid': True})
