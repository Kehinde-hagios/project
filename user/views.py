from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .decorator import redirect_authenticated_user
from django.contrib.auth.decorators import login_required
from .models import *

@redirect_authenticated_user
def register(request):
    if request.method == 'POST':
        form = registration_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully')
            return redirect('blog_login')
        
    else:
        form = registration_form()        
    
    return render(request, 'other/register.html', {'form':form})

@redirect_authenticated_user
def login(request):
    if request.method == 'POST':
        form = login_form(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    auth_login(request, user)
                    return redirect('blog_home') # Replace 'home' with your desired redirect
                else:
                    messages.error(request, 'Invalid email or password.')
            except User.DoesNotExist:
                messages.error(request, 'User with this email does not exist.')
            
    else:
        form = login_form()
        
    return render(request, 'other/login.html', {'form':form})
    
def logout(request):
    auth_logout(request)
    return redirect('blog_home') 

@login_required(login_url= 'blog_login')
def profile_info(request): 
    if request.method == 'POST':
        u_form = user_update_form(request.POST, instance=request.user)
        p_form = profile_update_form(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('blog_profile')
    else:
        u_form = user_update_form(instance=request.user)
        p_form = profile_update_form()
          
    context = {
        'u_form': u_form,
        'p_form': p_form
    }  
    
    return render(request, 'other/profile.html', context)