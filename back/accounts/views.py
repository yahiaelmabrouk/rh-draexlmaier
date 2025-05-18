from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import User
from .forms import ManagerCreateForm, ManagerPasswordChangeForm
import random
import string

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_manager(user):
    return user.is_authenticated and user.role == 'manager'

def is_admin_or_manager(user):
    return user.is_authenticated and user.role in ('admin', 'manager')

def login_view(request):
    msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect both admin and manager to data
            if user.role in ('admin', 'manager'):
                return redirect('data')
        else:
            msg = 'Invalid credentials. Please try again.'
    return render(request, 'accounts/login.html', {'msg': msg})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def dashboard(request):
    # Add a context variable for debugging
    return render(request, 'accounts/dashboard.html', {'test_message': 'Dashboard Page'})

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def manager_list(request):
    managers = User.objects.filter(role='manager')
    no_managers = not managers.exists()
    return render(request, 'accounts/manager_list.html', {
        'managers': managers,
        'no_managers': no_managers
    })

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def manager_add(request):
    if request.method == 'POST':
        form = ManagerCreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            country = form.cleaned_data['country']
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            user = User.objects.create_manager(name=name, email=email, country=country, password=password)
            # Send email
            subject = "Welcome to the platform"
            message = f"Hello {name},\n\nWelcome to our platform!\nYour login credentials:\nEmail: {email}\nPassword: {password}\n\nPlease change your password after login."
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            return redirect('manager_list')
    else:
        form = ManagerCreateForm()
    return render(request, 'accounts/manager_add.html', {'form': form})

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def manager_edit(request, pk):
    manager = get_object_or_404(User, pk=pk, role='manager')
    if request.method == 'POST':
        form = ManagerCreateForm(request.POST, instance=manager)
        if form.is_valid():
            form.save()
            return redirect('manager_list')
    else:
        form = ManagerCreateForm(instance=manager)
    return render(request, 'accounts/manager_edit.html', {'form': form, 'manager': manager})

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def manager_delete(request, pk):
    manager = get_object_or_404(User, pk=pk, role='manager')
    if request.method == 'POST':
        manager.delete()
        return redirect('manager_list')
    return render(request, 'accounts/manager_delete_confirm.html', {'manager': manager})

@login_required(login_url='login')
@user_passes_test(is_admin_or_manager, login_url='login')
def data(request):
    # Render the dashboard overview page (data.html)
    return render(request, 'accounts/data.html')

@login_required(login_url='login')
def dashboards(request):
    # Render the actual dashboards with PowerBI iframe
    return render(request, 'accounts/dashboard.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'accounts/about.html')

@login_required(login_url='login')
@user_passes_test(is_manager, login_url='login')
def manager_welcome(request):
    return redirect('data')

@login_required(login_url='login')
@user_passes_test(is_manager, login_url='login')
def manager_change_password(request):
    if request.method == 'POST':
        form = ManagerPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was changed successfully.')
            return redirect('manager_change_password')
    else:
        form = ManagerPasswordChangeForm(user=request.user)
    return render(request, 'accounts/manager_change_password.html', {'form': form})
