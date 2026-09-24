from functools import wraps
from django.shortcuts import redirect

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get("user_id"):
            return view_func(request, *args, **kwargs)
        return redirect("login")
    return wrapper
