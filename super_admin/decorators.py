from django.http import HttpResponse
from django.shortcuts import redirect


def is_admin_user(view_func):
    def wrapper_func(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('super_login')
        if not request.user.admin:
            return redirect('super_login')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
