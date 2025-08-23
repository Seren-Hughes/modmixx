from django.db import models
from django.conf import settings
from tracks.models import Track


# Create your models here.
class CommentManager(models.Manager):
    def visible(self):
        """
        Custom manager for Comment model.

        Provides filtering methods for comment visibility and moderation.
        """
        return self.filter(deleted=False)


class Comment(models.Model):
    """
    Comment model with soft deletion and threaded reply support.

    Supports hierarchical commenting system with parent-child relationships.
    Implements soft deletion to preserve reply structure when comments
    are removed. Includes moderation fields for content review.

    Fields:
        user: ForeignKey to CustomUser (comment author)
        track: ForeignKey to Track (commented track)
        content: TextField max 1000 chars (comment text)
        created_at: DateTimeField (auto-generated creation timestamp)
        updated_at: DateTimeField (auto-updated modification timestamp)
        is_approved: BooleanField (moderation approval status)
        needs_review: BooleanField (flagged for manual review)
        parent: ForeignKey to self (threaded replies support)
        deleted: BooleanField (soft deletion flag)

    Related Models:
        CustomUser: ForeignKey (comment.user)
        Track: ForeignKey (comment.track)
        Comment: Self-referential ForeignKey (replies relationship)

    Deletion Strategy:
        - Soft delete if comment has replies (preserves thread structure)
        - Hard delete if no replies (complete removal)
        - Recursive cleanup of soft-deleted parents when replies are gone

    Moderation:
        - Perspective API toxicity checking via CommentForm
        - Manual review flags for community reporting
        - Admin interface for bulk moderation actions
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    track = models.ForeignKey(
        Track, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)  # For moderation
    needs_review = models.BooleanField(default=False)  # For flagged comments
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE,
    )
    deleted = models.BooleanField(default=False)

    objects = CommentManager()

    def __str__(self):
        return f"{self.user} on {self.track}: {self.content[:30]}"

    class Meta:
        ordering = ["-created_at"]

    def get_visible_replies(self):
        """Get non-deleted replies for this comment"""
        return self.replies.filter(deleted=False)
