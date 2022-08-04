from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

def super_login(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home_super')
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                if user.is_admin:
                    login(request, user)
                    return redirect('home_super')
                else:
                    messages.error(request, "only Admin credential required")
                    return redirect('super_login')
            else:
                messages.error(request, "invalid credential try again")
                return redirect('super_login')
        else:
            messages.error(request, "All fields are required")
            return redirect('super_login')

    return render(request, 'super_login.html')


def home_super(request):
    return render(request, 'home_super.html')
