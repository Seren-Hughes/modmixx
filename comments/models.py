from django.db import models
from django.conf import settings
from tracks.models import Track

# Create your models here.
class CommentManager(models.Manager):
    def visible(self):
        """Return only non-deleted comments"""
        return self.filter(deleted=False)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)  # For moderation
    needs_review = models.BooleanField(default=False) # For flagged comments
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )
    deleted = models.BooleanField(default=False)

    objects = CommentManager()

    def __str__(self):
        return f"{self.user} on {self.track}: {self.content[:30]}" # Truncate for readability
    
    class Meta:
        ordering = ['-created_at']

    def get_visible_replies(self):
        """Get non-deleted replies for this comment"""
        return self.replies.filter(deleted=False)