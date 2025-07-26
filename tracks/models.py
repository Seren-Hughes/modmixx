from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.
class Track(models.Model):
    """
    Represents a music track.
    Attributes:
        title (str): The title of the track.
        slug (str): A unique slug for the track, auto-generated from the title.
        description (str): A brief description of the track.
        audio_file (FileField): The audio file of the track.
        track_image (ImageField): An optional image associated with the track.
        user (ForeignKey): The user who uploaded the track.
        tags (str): Comma-separated tags for the track.
        created_at (DateTimeField): Timestamp when the track was created.
        updated_at (DateTimeField): Timestamp when the track was last updated.
    Methods:
        save(): Auto-generates a slug from the title if not provided.

    """
    # Basic track information
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    # File and image fields
    audio_file = models.FileField(upload_to='tracks/')
    track_image = models.ImageField(upload_to='track_images/', blank=True, null=True)

    # User who uploaded the track
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tracks')
    
    # Additional metadata
    tags = models.CharField(max_length=200, blank=True)

     # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] # Newest tracks first

    def __str__(self):
        return f"{self.title} by {self.user.profile.display_name or self.user.profile.username}"
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Ensure slug is unique by adding counter if needed
            while Track.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs) 