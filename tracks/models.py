from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.uploadedfile import UploadedFile
import os

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
    audio_file = models.FileField(upload_to='tracks/', blank=True)
    track_image = models.ImageField(upload_to='track_images/', blank=True, null=True)

    # User who uploaded the track
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tracks')

     # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Moderation fields
    MOD_STATUS = (("PENDING","Pending"), ("APPROVED","Approved"), ("REJECTED","Rejected"))
    moderation_status = models.CharField(max_length=9, choices=MOD_STATUS, default="PENDING")
    moderation_labels = models.JSONField(blank=True, null=True)
    moderated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at'] # Newest tracks first

    def __str__(self):
        return f"{self.title} by {self.user.profile.display_name or self.user.profile.username}"
    
    def save(self, *args, **kwargs):
        # Generate slug from title if not provided OR if title has changed
        if not self.slug or (self.pk and self.title):
            # For existing tracks, check if title changed
            if self.pk:
                try:
                    old_track = Track.objects.get(pk=self.pk)
                    if old_track.title != self.title:
                        # Title changed, regenerate slug
                        base_slug = slugify(self.title)
                        slug = base_slug
                        counter = 1
                        while Track.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                            slug = f"{base_slug}-{counter}"
                            counter += 1
                        self.slug = slug
                except Track.DoesNotExist:
                    pass
            else:
                # New track, generate slug
                base_slug = slugify(self.title)
                slug = base_slug
                counter = 1
                while Track.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs) 


    def get_audio_filename(self):
        """Return just the filename without path."""
        if self.audio_file:
            return os.path.basename(self.audio_file.name)
        return "No file"
    
    def get_image_filename(self):
        """Return just the image filename without path."""
        if self.track_image:
            return os.path.basename(self.track_image.name)
        return "No image"
    
    
    
# Signal handler to delete files from S3 when a Track is deleted    
@receiver(post_delete, sender=Track)
def delete_files_on_track_delete(sender, instance, **kwargs):
    """Delete audio and image files from S3 when a Track instance is deleted.
    Args:
        sender (Model): The model class that sent the signal.
        instance (Track): The instance of the Track being deleted.
        **kwargs: Additional keyword arguments.
    """
    # Check if the instance has audio_file and track_image, then delete them
    if instance.audio_file:
        instance.audio_file.delete(save=False)
    if instance.track_image:
        instance.track_image.delete(save=False)