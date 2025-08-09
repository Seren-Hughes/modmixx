from django import forms
from django.utils import timezone
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import re
import os
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from core.utils import get_toxicity_score 
from ulid import ULID
from tracks.services.moderation import scan_image_bytes 

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)

class ProfileForm(forms.ModelForm):
    """Form for creating and editing user profiles.
       Applies XSS/HTML injection protection and file upload security.
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

    def clean_display_name(self):
        display_name = self.cleaned_data.get('display_name')
        if display_name:
            display_name = display_name.strip()
            # Remove HTML tags
            if re.search(r'<[^>]*>', display_name):
                raise ValidationError("HTML tags are not allowed in display name.")
            # Check for dangerous patterns
            dangerous_patterns = [
                'javascript:', 'vbscript:', 'onclick=', 'onerror=', 'onload=',
                'onmouseover=', 'onfocus=', 'data:', 'script'
            ]
            display_name_lower = display_name.lower()
            for pattern in dangerous_patterns:
                if pattern in display_name_lower:
                    raise ValidationError(
                        f"Display name contains potentially harmful content: '{pattern}'."
                    )
            # Perspective API moderation
            try:
                toxicity = get_toxicity_score(display_name)
                if toxicity > 0.7:
                    raise ValidationError("Your display name may contain inappropriate language. Please revise.")
            except ValidationError:
                raise
            except Exception:
                pass  # Allow if API fails
            if len(display_name) > 100:
                raise ValidationError("Display name too long. Maximum 100 characters.")
        return display_name

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if bio:
            bio = bio.strip()
            # Remove HTML tags
            if re.search(r'<[^>]*>', bio):
                raise ValidationError("HTML tags are not allowed in bio.")
            # Check for dangerous patterns
            dangerous_patterns = [
                'javascript:', 'vbscript:', 'onclick=', 'onerror=', 'onload=',
                'onmouseover=', 'onfocus=', 'data:', 'script'
            ]
            bio_lower = bio.lower()
            for pattern in dangerous_patterns:
                if pattern in bio_lower:
                    raise ValidationError(
                        f"Bio contains potentially harmful content: '{pattern}'."
                    )
            # Perspective API moderation
            try:
                toxicity = get_toxicity_score(bio)
                if toxicity > 0.7:
                    raise ValidationError("Your bio may contain inappropriate language. Please revise.")
            except ValidationError:
                raise
            except Exception:
                pass  # Allow if API fails
            if len(bio) > 500:
                raise ValidationError("Bio too long. Maximum 500 characters.")
        return bio

    def clean_pronouns(self):
        pronouns = self.cleaned_data.get('pronouns')
        if pronouns:
            pronouns = pronouns.strip()
            # Remove HTML tags
            if re.search(r'<[^>]*>', pronouns):
                raise ValidationError("HTML tags are not allowed in pronouns.")
            # Check for dangerous patterns
            dangerous_patterns = [
                'javascript:', 'vbscript:', 'onclick=', 'onerror=', 'onload=',
                'onmouseover=', 'onfocus=', 'data:', 'script'
            ]
            pronouns_lower = pronouns.lower()
            for pattern in dangerous_patterns:
                if pattern in pronouns_lower:
                    raise ValidationError(
                        f"Pronouns contain potentially harmful content: '{pattern}'."
                    )
            # Perspective API moderation
            try:
                toxicity = get_toxicity_score(pronouns)
                if toxicity > 0.7:
                    raise ValidationError("Your pronouns may contain inappropriate language. Please revise.")
            except ValidationError:
                raise
            except Exception:
                pass  # Allow if API fails
            if len(pronouns) > 50:
                raise ValidationError("Pronouns too long. Maximum 50 characters.")
        return pronouns

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise ValidationError("Username cannot contain spaces")
        # Remove HTML tags
        if re.search(r'<[^>]*>', username):
            raise ValidationError("HTML tags are not allowed in username.")
        # Check for dangerous patterns
        dangerous_patterns = [
            'javascript:', 'vbscript:', 'onclick=', 'onerror=', 'onload=',
            'onmouseover:', 'onfocus=', 'data:', 'script'
        ]
        username_lower = username.lower()
        for pattern in dangerous_patterns:
            if pattern in username_lower:
                raise ValidationError(
                    f"Username contains potentially harmful content: '{pattern}'."
                )
        return username.lower()

    def clean_profile_picture(self):
        """
        Security validation for newly uploaded profile pictures only.
        - File size: 20MB max
        - Extension: jpg, jpeg, png, webp
        - MIME type: image/jpeg, image/png, image/webp
        - Filename sanitization with ULID for uniqueness
        - AWS Rekognition content moderation
        """
        image = self.cleaned_data.get('profile_picture')
        
        # Initialize moderation flags
        self._moderation_failed = False
        self._moderation_allowed = True
        self._moderation_labels = []
        
        # Only validate if a new file is uploaded
        if isinstance(image, (InMemoryUploadedFile, TemporaryUploadedFile)):
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
            
            # AWS Rekognition content moderation
            try:
                data = image.read()
                image.seek(0)  # Reset file pointer for storage
                
                allowed, labels, failed = scan_image_bytes(data)
                self._moderation_allowed = allowed
                self._moderation_labels = labels
                self._moderation_failed = failed
                
                if not allowed:
                    raise ValidationError("This image violates our community guidelines.")
                    
            except ValidationError:
                raise  # Re-raise validation errors
            except Exception:
                # Fail-open: allow upload but mark as pending
                self._moderation_failed = True
            
            # Generate unique filename with ULID 
            name, ext = os.path.splitext(filename)
            safe_name = ''.join(c for c in name if c.isalnum() or c in ' -_()[]')
            safe_name = safe_name.strip()[:30]
            
            if safe_name:
                ulid = str(ULID())
                image.name = f"{safe_name}_{ulid}{ext}"
            else:
                ulid = str(ULID())
                image.name = f"profile_{ulid}{ext}"
            
        return image

    def save(self, commit=True):
        """
        Save profile with moderation status based on image scan results.
        """
        profile = super().save(commit=False)
        
        # Set moderation status if image was processed
        if hasattr(self, '_moderation_failed') or hasattr(self, '_moderation_allowed'):
            if getattr(self, '_moderation_failed', False):
                profile.moderation_status = "PENDING"
                profile.moderation_labels = None
            else:
                profile.moderation_status = "APPROVED" if getattr(self, '_moderation_allowed', True) else "REJECTED"
                profile.moderation_labels = getattr(self, '_moderation_labels', [])
            profile.moderated_at = timezone.now()
        
        if commit:
            profile.save()
        return profile