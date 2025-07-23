from django import forms
from .models import Profile

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class ProfileForm(forms.ModelForm):
    """Form for creating and editing user profiles.
    Fields:
        username: Unique username for the profile.
        display_name: Name displayed to others.
        bio: Short biography or description.
        pronouns: User's preferred pronouns.
        profile_picture: Optional profile image.
    """
    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'bio', 'pronouns', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Different help text for new vs existing profiles
        if self.instance.pk:  # Editing existing profile
            self.fields['username'].help_text = "Warning! Changing this will break any existing URL links to your profile."
        else:  # Creating new profile
            self.fields['username'].help_text = "Choose your unique profile URL (letters, numbers, hyphens, underscores only)"
        
        # Set error message for both cases
        self.fields['username'].error_messages = {
            'invalid': 'Username can only contain letters, numbers, hyphens, and underscores'
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError("Username cannot contain spaces")
        return username.lower()  # Ensure lowercase