from django.db import models
from django.conf import settings
from tracks.models import Track

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)  # For moderation
    needs_review = models.BooleanField(default=False) # For flagged comments

    def __str__(self):
        return f"{self.user} on {self.track}: {self.content[:30]}"
    
    class Meta:
        ordering = ['-created_at']