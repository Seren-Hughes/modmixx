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
        
    def clean_audio_file(self):
        audio_file = self.cleaned_data.get('audio_file')
        if audio_file:
            # Validate file size (max 50MB) 
            if audio_file.size > 50 * 1024 * 1024:
                raise forms.ValidationError('Audio file too large (max 50MB)')
        return audio_file 