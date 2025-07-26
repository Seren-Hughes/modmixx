from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from tracks.models import Track
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
            return redirect('profile', username=request.user.profile.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile_setup.html', {'form': form})


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.profile.username)
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
    
    if not user.profile.username:
        return redirect('profile_setup')
    
    return redirect('profile', username=user.profile.username)

@login_required
def profile(request, username):
    """
    Display profile view for any user by username.
    Shows edit options if viewing your own profile.
    Display user profile track uploads.
    """
    profile = get_object_or_404(Profile, username=username)

    # Get user's tracks ordered by newest first
    user_tracks = Track.objects.filter(user=profile.user).order_by('-created_at')
    
    context = {
        'profile': profile,
        'is_owner': request.user == profile.user,
        'user_tracks': user_tracks,
    }
    
    # If the user is viewing their own profile, they can edit it
    if request.user == profile.user:
        
        pass # handle edit logic here if needed 
    
    return render(request, 'accounts/profile.html', context)