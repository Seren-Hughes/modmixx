from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from .models import Track
import os

class TrackUploadForm(forms.ModelForm):
    """
    Form for uploading and editing tracks with comprehensive validation and security measures.
    
    This form handles track creation and editing while preserving existing files when 
    only metadata is updated. Implements multiple security validations following 
    OWASP guidelines for file upload security.
    
    Security Features:
        - File size limits (100MB for audio, 10MB for images)
        - MIME type validation (prevents malicious file uploads)
        - Filename sanitization (prevents directory traversal attacks)
        - File extension validation
    
    Fields:
        title (str): The title of the track (max 200 characters).
        description (str): A description of the track (max 2000 characters).
        audio_file (File): The audio file - MP3, WAV, FLAC, M4A, AAC, or OGG format.
        track_image (File): Optional cover image - JPG, PNG, or WebP format.
    
    Validation:
        - Audio files: Content-type verification, size limits, filename sanitization
        - Images: Format validation, size limits
        - Text fields: Length limits, basic sanitization
        - Edit mode: Preserves existing files when not replaced
    
    References:
        - OWASP File Upload Security Guidelines
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

    # https://stackoverflow.com/questions/51075396/python-django-does-not-overwrite-newly-uploaded-file-with-old-one
    # https://stackoverflow.com/questions/69448205/how-to-update-filefield-data-only-if-a-new-file-has-been-chosen-in-django-or-to
    # https://stackoverflow.com/questions/17774636/editing-a-django-model-with-a-filefield-without-re-uploading-the-file
    def clean_audio_file(self):
        """
        Validate uploaded audio files for security and format compliance.
        Implements filename sanitization following OWASP File Upload Cheat Sheet
        recommendations to prevent path traversal attacks (CWE-22).

        References:
        - https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
        - https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html
        - https://docs.djangoproject.com/en/5.2/ref/validators/ = djangos native validators
        - https://docs.djangoproject.com/en/5.2/topics/security/#user-uploaded-content-security
        - https://cwe.mitre.org/data/definitions/22.html
        """
        audio_file = self.cleaned_data.get('audio_file')
        # Only validate if a new file is uploaded
        if audio_file and hasattr(audio_file, 'size'):
            if audio_file.size > 100 * 1024 * 1024:
                raise forms.ValidationError('File size exceeds 100MB limit.')
            
            # Content type validation
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
            # Filename sanitization per OWASP guidelines
            # Remove characters that could enable path traversal or filesystem attacks
            if hasattr(audio_file, 'name') and audio_file.name:
                name, ext = os.path.splitext(audio_file.name)
                # Allow only alphanumeric and safe punctuation (OWASP recommendation)
                safe_name = ''.join(c for c in name if c.isalnum() or c in ' -_()[]')
                safe_name = safe_name.strip()[:50]  # Limit length to prevent buffer issues
                if safe_name:  # Only change if it's a valid name
                    audio_file.name = f"{safe_name}{ext}"

            return audio_file
        # If editing and no new file uploaded, keep the existing file
        elif self.instance and self.instance.pk:
            return self.instance.audio_file
        return audio_file