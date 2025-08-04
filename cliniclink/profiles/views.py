from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'profiles/index.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            UserProfile.objects.create(
                user=user,
                user_type=form.cleaned_data['user_type'],
                profile_picture=form.cleaned_data.get('profile_picture'),
                address_line1=form.cleaned_data['address_line1'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                pincode=form.cleaned_data['pincode']
            )
            return redirect('login')
    else:
        form = SignupForm()
    
    context = {
        'form' : form
    }
    return render(request, 'profiles/signup.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            profile = UserProfile.objects.get(user=user)
            if profile.user_type == 'patient':
                return redirect('patient_dashboard')
            else:
                return redirect('doctor_dashboard')
    return render(request, 'profiles/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def patient_dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    if profile.user_type != 'Patient':
        return redirect('doctor_dashboard')
    
    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'profiles/patient_dashboard.html', context)

@login_required
def doctor_dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    if profile.user_type != 'Doctor':
        return redirect('patient_dashboard')
    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'profiles/doctor_dashboard.html', context)
