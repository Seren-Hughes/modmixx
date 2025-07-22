from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import login

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # Create a profile for the new user
            login(request, user)  # Log the user in
            return redirect('profile_setup')  # Redirect to a profile setup page or login
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile_setup(request):

    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile_setup.html', {'form': form})

@login_required
def profile_detail(request):
    return render(request, 'accounts/profile_detail.html', {'profile': request.user.profile})


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def login_redirect(request):
    """
    Redirect users after login:
    - New users (no profile or incomplete profile) -> profile setup
    - Existing users with complete profiles -> profile page
    """
    user = request.user

    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
        return redirect('profile_setup')
    
    return redirect('profile_detail')