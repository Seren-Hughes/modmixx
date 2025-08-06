from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .models import Profile
from tracks.models import Track
from django.contrib.auth import login, logout
from django.core.mail import send_mail

# Create your views here.
def signup(request):
    """Handle user registration with email and password."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                Profile.objects.create(user=user)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                # Send welcome email
                send_mail(
                    subject="Welcome to modmixx 🎉",
                    message=(
                        "Thanks for signing up to modmixx!\n\n"
                        "We're thrilled to have you in our collaborative music community. "
                        "Dive in, explore, and start creating!"
                    ),
                    from_email="modmixx.platform@gmail.com",
                    recipient_list=[user.email],
                    fail_silently=True,
                )
                
            except Exception as e:
                # Log error but don't break signup process
                print(f"Signup error: {e}")
                
            return redirect('profile_setup')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile_setup(request):
    """Handle initial profile setup for new users."""
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == "POST":
        # Store reference to old profile image before form processing
        old_profile_image = request.user.profile.profile_picture if request.user.profile.profile_picture else None
        
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            # Save the updated profile
            updated_profile = form.save()
            
            # Delete old profile image if a new one was uploaded
            if 'profile_picture' in form.changed_data and old_profile_image:
                if old_profile_image != updated_profile.profile_picture:
                    old_profile_image.delete(save=False)
            
            return redirect('profile', username=request.user.profile.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile_setup.html', {'form': form})

@login_required
def profile_edit(request):
    """Handle profile editing for existing users."""
    if request.method == "POST":
        # Store reference to old profile image before form processing
        old_profile_image = request.user.profile.profile_picture if request.user.profile.profile_picture else None
        
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            # Save the updated profile
            updated_profile = form.save()
            
            # Delete old profile image if a new one was uploaded
            if 'profile_picture' in form.changed_data and old_profile_image:
                if old_profile_image != updated_profile.profile_picture:
                    old_profile_image.delete(save=False)
            
            return redirect('profile', username=request.user.profile.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def login_redirect(request):
    """
    Redirect users after login based on profile completion status.
    
    - New users (no profile or incomplete profile) -> profile setup
    - Existing users with complete profiles -> their profile page
    """
    user = request.user

    # Create profile if it doesn't exist
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
        return redirect('profile_setup')
    
    # Redirect to setup if username is missing
    if not user.profile.username:
        return redirect('profile_setup')
    
    # Redirect to user's profile
    return redirect('profile', username=user.profile.username)

@login_required
def profile(request, username):
    """Display public profile view for any user."""
    profile = get_object_or_404(Profile, username=username)
    user_tracks = Track.objects.filter(user=profile.user).order_by('-created_at')
    
    context = {
        'profile': profile,
        'is_owner': request.user == profile.user,
        'user_tracks': user_tracks,
    }
    
    return render(request, 'accounts/profile.html', context)

class CustomPasswordResetView(auth_views.PasswordResetView):
    """Custom password reset view with branded from_email."""
    from_email = "modmixx.platform@gmail.com"
    template_name = 'accounts/password_reset.html'

@login_required
def account_delete(request):
    """Handle account deletion with confirmation."""
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')
    return render(request, 'accounts/account_delete_confirm.html')

def custom_logout(request):
    """Handle user logout and redirect to home page."""
    logout(request)
    return render(request, 'accounts/logout.html')