from django import forms
from .models import Track

class TrackUploadForm(forms.ModelForm):
    """
    Form for uploading a new track with fields for title, description, audio file,
    track image, and tags.
    This form includes validation for the audio file size.
    
    Attributes:
        title (str): The title of the track.
        description (str): A brief description of the track.
        audio_file (File): The audio file of the track.
        track_image (File): An optional image for the track.
        tags (str): Comma-separated tags for categorizing the track.

    """
    class Meta:
        model = Track
        fields = ['title', 'description', 'audio_file', 'track_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Track title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Describe your track...'
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
            audio_file = self.cleaned_data.get('audio_file')
            # Only validate if a new file is uploaded
            if audio_file and hasattr(audio_file, 'size'):
                if audio_file.size > 50 * 1024 * 1024:
                    raise forms.ValidationError('Audio file too large (max 50MB)')
                return audio_file
            # If editing and no new file uploaded, keep the existing file
            elif self.instance and self.instance.pk:
                return self.instance.audio_file
            return audio_file