from django import forms
from .models import Profile

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re
from django.core.exceptions import ValidationError

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

    def clean_profile_picture(self):
        image = self.cleaned_data.get('profile_picture')

        # Only validate if a new file is uploaded 
        if image and hasattr(image, 'file'):
            # File size validation (20MB limit)
            if image.size > 20 * 1024 * 1024:
                raise ValidationError("Image file too large. Maximum size is 20MB.")

            # File extension validation (case-insensitive)
            allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
            filename = image.name.split('/')[-1].split('\\')[-1]
            ext = filename.split('.')[-1].lower() if '.' in filename else ''
            if ext not in allowed_extensions:
                raise ValidationError("Invalid file type. Only JPG, PNG, and WebP files are allowed.")

            # MIME type validation
            allowed_types = ['image/jpeg', 'image/png', 'image/webp']
            if hasattr(image, 'content_type') and image.content_type not in allowed_types:
                raise ValidationError("Invalid image format. Only JPG, PNG, and WebP are allowed.")

            # Basic filename sanitization
            if '..' in filename or '/' in filename or '\\' in filename:
                raise ValidationError("Invalid filename.")
            safe_name = re.sub(r'[^\w\-_\.]', '', filename)
            if safe_name != filename:
                image.name = safe_name

        return image