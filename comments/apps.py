from django.apps import AppConfig


class CommentsConfig(AppConfig):
    """
    Configuration for the comments Django app.

    Handles threaded comment system with soft deletion and content
    moderation via Google's Perspective API. Supports AJAX-based
    commenting to prevent audio playback interruption.

    Features:
        - Threaded replies with parent-child relationships
        - Soft deletion preserving reply structure
        - Automatic toxicity detection and blocking
        - AJAX comment posting and editing
        - Recursive parent cleanup on hard deletion
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "comments"
