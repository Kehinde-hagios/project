from django.shortcuts import redirect

def redirect_authenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog_home')  # 👈 Change to your homepage URL name
        return view_func(request, *args, **kwargs)
    return wrapper
