from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import (
    get_user_model
)


def redirect_authenticated_user(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.deactivated_at:
                return redirect("active_index")
            if request.user.is_first:
                return redirect("active_first_time_user")
            return redirect("active_index")
        else:
            return view(request, *args, **kwargs)
    return wrapper

def only_authenticated_user(view, redirect_to='login'):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect(redirect_to)
        else:
            return view(request, *args, **kwargs)
    return wrapper
