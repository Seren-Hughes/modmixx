from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from core.utils import get_toxicity_score
from .models import Track
import os
import re # Regular expressions module for filename sanitization

class TrackUploadForm(forms.ModelForm):
    """
    Form for uploading and editing tracks with comprehensive validation and security measures.
    
    This form handles track creation and editing while preserving existing files when 
    only metadata is updated. Implements multiple security validations following 
    OWASP guidelines for file upload security and XSS prevention.
    
    Security Features:
        - File size limits (100MB for audio, 10MB for images)
        - MIME type validation (prevents malicious file uploads)
        - Filename sanitization (prevents directory traversal attacks)
        - XSS prevention through input validation
        - HTML injection protection
    
    Fields:
        title (str): The title of the track (max 200 characters).
        description (str): A description of the track (max 2000 characters).
        audio_file (File): The audio file - MP3, WAV, FLAC, M4A, AAC, or OGG format.
        track_image (File): Optional cover image - JPG, PNG, or WebP format.
    
    Validation:
        - Audio files: Content-type verification, size limits, filename sanitization
        - Images: Format validation, size limits, dimension checks
        - Text fields: XSS prevention, HTML tag filtering, length limits
        - Edit mode: Preserves existing files when not replaced
    
    References:
        - OWASP File Upload Security Guidelines
        - OWASP XSS Prevention Cheat Sheet
        - Django Security Best Practices
    """
    audio_file = forms.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=['mp3', 'wav', 'flac', 'm4a', 'aac', 'ogg']
            ),
        ],
        help_text="Supported formats: MP3, WAV, FLAC, M4A, AAC, OGG (max 100MB)",
        widget=forms.FileInput(attrs={
            'accept': 'audio/*',
            'class': 'form-control'
        })
    )
    
    track_image = forms.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'webp']
            ),
        ],
        help_text="Optional track image: JPG, PNG, WebP (max 10MB)",
        widget=forms.FileInput(attrs={
            'accept': 'image/*',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Track
        fields = ['title', 'description', 'audio_file', 'track_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Track title',
                'maxlength': 200
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Describe your track...',
                'maxlength': 2000
            }),
            'audio_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'audio/*'
            }),
            'track_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If this is an edit (instance exists), make file fields not required
        if self.instance and self.instance.pk:
            self.fields['audio_file'].required = False
            self.fields['track_image'].required = False

    # https://stackoverflow.com/questions/51075396/python-django-does-not-overwrite-newly-uploaded-file-with-old-one
    # https://stackoverflow.com/questions/69448205/how-to-update-filefield-data-only-if-a-new-file-has-been-chosen-in-django-or-to
    # https://stackoverflow.com/questions/17774636/editing-a-django-model-with-a-filefield-without-re-uploading-the-file
    def clean_audio_file(self):
        """
        Validate uploaded audio files for security and format compliance.
        
        Implements comprehensive validation following OWASP File Upload Guidelines
        to prevent malicious uploads and ensure proper file handling.
        
        Security measures:
            - File size validation (100MB limit)
            - MIME type verification (prevents format spoofing)
            - Filename sanitization (prevents path traversal attacks - CWE-22)
            - Extension validation (handled by FileExtensionValidator)
        
        Returns:
            File: Validated and sanitized audio file, or existing file for edits
            
        Raises:
            ValidationError: If file fails security or format validation
            
        References:
        - https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
        - https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html
        - https://docs.djangoproject.com/en/5.2/ref/validators/ = djangos native validators
        - https://docs.djangoproject.com/en/5.2/topics/security/#user-uploaded-content-security
        - https://cwe.mitre.org/data/definitions/22.html
        """
        audio_file = self.cleaned_data.get('audio_file')

        # Check if this is an edit and the audio hasn't changed
        if self.instance and self.instance.pk:
            if not audio_file:
                return self.instance.audio_file
            elif hasattr(audio_file, 'name') and self.instance.audio_file:
                # Check if it's the same file (same name = no new upload)
                if audio_file.name == self.instance.audio_file.name:
                    return self.instance.audio_file
        
        # Only validate if a new audio file was uploaded
        if audio_file and hasattr(audio_file, 'file'):
            # File size validation - prevent resource exhaustion
            if audio_file.size > 100 * 1024 * 1024:
                raise forms.ValidationError('File size exceeds 100MB limit.')
            
            # MIME type validation - prevent format spoofing attacks
            allowed_content_types = [
                'audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/x-wav',
                'audio/flac', 'audio/mp4', 'audio/aac', 'audio/ogg',
                'audio/x-m4a'  
            ]
            if hasattr(audio_file, 'content_type') and audio_file.content_type:
                if audio_file.content_type not in allowed_content_types:
                    raise forms.ValidationError(
                        f'Invalid audio file type: {audio_file.content_type}. '
                        'Please upload MP3, WAV, FLAC, M4A, AAC, or OGG files.'
                    )
            
            # Filename sanitization following OWASP recommendations
            # Prevents path traversal and filesystem attacks
            if hasattr(audio_file, 'name') and audio_file.name:
                name, ext = os.path.splitext(audio_file.name)
                # Allow only alphanumeric characters and safe punctuation
                safe_name = ''.join(c for c in name if c.isalnum() or c in ' -_()[]')
                safe_name = safe_name.strip()[:50]  # Limit length to prevent buffer issues
                if safe_name:
                    audio_file.name = f"{safe_name}{ext}"

            return audio_file
        
        return audio_file

    def clean_track_image(self):
        """    
        Validate uploaded track images for security and format compliance.
        
        Implements comprehensive image validation to prevent malicious uploads
        and ensure proper resource management.
    
        Security measures:
            - File size validation (10MB limit)
            - Image format verification (JPG, PNG, WebP only)
            - Dimension limits (prevents resource exhaustion)
            - Filename sanitization (prevents path traversal attacks)
            
        Returns:
            ImageFile: Validated and sanitized image file, or existing file for edits
            
        Raises:
            ValidationError: If image fails security or format validation
        """
        track_image = self.cleaned_data.get('track_image')
        
        # Check if this is an edit and the image hasn't changed
        if self.instance and self.instance.pk:
            if not track_image:
                # No image uploaded, return existing
                return self.instance.track_image
            elif hasattr(track_image, 'name') and self.instance.track_image:
                # Check if it's the same file (same name = no new upload)
                if track_image.name == self.instance.track_image.name:
                    return self.instance.track_image
        
        # Only validate if a new image was uploaded
        if track_image and hasattr(track_image, 'file'):
            # Image size validation - prevent resource exhaustion
            if track_image.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError('Image too large (max 10MB)')
            
            # MIME type validation - prevent format spoofing
            allowed_image_types = [
                'image/jpeg', 'image/jpg', 'image/png', 'image/webp'
            ]
            if hasattr(track_image, 'content_type') and track_image.content_type:
                if track_image.content_type not in allowed_image_types:
                    raise forms.ValidationError(
                        'Invalid image type. Please upload JPG, PNG, or WebP files.'
                    )
            
            # Image dimension validation - prevent resource exhaustion
            if hasattr(track_image, 'width') and hasattr(track_image, 'height'):
                if track_image.width > 2000 or track_image.height > 2000:
                    raise forms.ValidationError(
                        'Image dimensions too large. Maximum 2000x2000 pixels.'
                    )
                
            # Filename sanitization following OWASP recommendations
            if hasattr(track_image, 'name') and track_image.name:
                name, ext = os.path.splitext(track_image.name)
                # Allow only alphanumeric characters and safe punctuation
                safe_name = ''.join(c for c in name if c.isalnum() or c in ' -_()[]')
                safe_name = safe_name.strip()[:50]  # Limit length to prevent buffer issues
                if safe_name:
                    track_image.name = f"{safe_name}{ext}"    
        
        # return the image as-is
        return track_image

    def clean_title(self):
        """
        Validate track title for security, format compliance and content moderation using Perspective API.

        Implements comprehensive input validation following OWASP guidelines
        to prevent Cross-Site Scripting (XSS) and injection attacks.
        Blocks titles with toxicity score above 0.7 threshold.
        
        Security measures:
            - HTML tag detection and rejection
            - JavaScript protocol filtering (javascript:, vbscript:)
            - Event handler detection (onclick, onerror, etc.)
            - Script content filtering
            - Length validation
        
        Returns:
            str: Validated and sanitized title
            
        Raises:
            ValidationError: If title contains malicious content or is invalid
            
        References:
            - OWASP XSS Prevention: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
            - OWASP Input Validation: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
        """
        title = self.cleaned_data.get('title')
        
        if title:
            title = title.strip()

            
            # Perspective API moderation
            try:
                toxicity = get_toxicity_score(title)
                if toxicity > 0.7:
                    raise ValidationError("Your track title may contain inappropriate language. Please revise.")
            except ValidationError:
                raise  # Re-raise validation errors
            except Exception as e:
                # Log API errors but allow track if moderation service fails
                print(f"Perspective API error for title: {e}")
                pass
            
            # Length validation
            if len(title) < 2:
                raise forms.ValidationError("Title must be at least 2 characters.")
            
            # HTML tag detection - prevents XSS through markup injection
            if re.search(r'<[^>]*>', title):
                raise forms.ValidationError(
                    "HTML tags are not allowed in titles."
                )
            
            # Dangerous pattern detection - prevents script injection attacks
            dangerous_patterns = [
                'javascript:', 'vbscript:', 'onclick=', 'onerror=', 'onload=',
                'onmouseover=', 'onfocus=', 'data:', 'script'
            ]
            
            title_lower = title.lower()
            for pattern in dangerous_patterns:
                if pattern in title_lower:
                    raise forms.ValidationError(
                        f"Title contains potentially harmful content: '{pattern}'. "
                        "Please remove any scripts or suspicious content."
                    )
        
        return title

    def clean_description(self):
        """
        Validate track description for security, content compliance and moderation using Perspective API.

        Implements comprehensive content filtering to prevent Cross-Site Scripting (XSS)
        and other injection attacks while maintaining usability for legitimate content.
        Blocks descriptions with toxicity score above 0.7 threshold.
        
        Security measures:
            - HTML tag detection and rejection
            - JavaScript protocol filtering
            - Event handler detection  
            - Script content filtering
            - Whitespace normalization
        
        Returns:
            str: Validated and sanitized description with normalized whitespace
            
        Raises:
            ValidationError: If description contains malicious content
            
        References:
            - OWASP XSS Prevention: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
            - OWASP Input Validation: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
            - CWE-79 XSS: https://cwe.mitre.org/data/definitions/79.html
        """
        description = self.cleaned_data.get('description')
        
        if description:
            description = description.strip()

            # Perspective API moderation
            try:
                toxicity = get_toxicity_score(description)
                if toxicity > 0.7:
                    raise ValidationError("Your track description may contain inappropriate language. Please revise.")
            except ValidationError:
                raise  # Re-raise validation errors
            except Exception as e:
                # Log API errors but allow track if moderation service fails
                print(f"Perspective API error for description: {e}")
                pass
            
            # HTML tag detection - prevents XSS through markup injection
            if re.search(r'<[^>]*>', description):
                raise forms.ValidationError(
                    "HTML tags are not allowed in descriptions."
                )
            
            # Dangerous pattern detection - prevents script injection attacks
            dangerous_patterns = [
                'javascript:', 'vbscript:', 'onclick=', 'onerror=', 'onload=',
                'onmouseover=', 'onfocus=', 'data:', 'script'
            ]
            
            description_lower = description.lower()
            for pattern in dangerous_patterns:
                if pattern in description_lower:
                    raise forms.ValidationError(
                        f"Description contains potentially harmful content: '{pattern}'. "
                        "Please remove any scripts or suspicious content."
                    )
            
            # Whitespace normalization - improves content consistency
            description = re.sub(r' +', ' ', description)  # Multiple spaces to single
            description = re.sub(r'\n\s*\n\s*\n', '\n\n', description)  # Max double newlines
        
        return description

# End of TrackUploadForm class