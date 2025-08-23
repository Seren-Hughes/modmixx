from django.apps import AppConfig


class TracksConfig(AppConfig):
    """
    Configuration for the tracks Django app.

    Manages music track uploads with comprehensive security validation,
    content moderation, and file management. Integrates AWS S3 storage
    and Rekognition for automated content review.

    Features:
        - Secure file upload with MIME type validation
        - AWS Rekognition image moderation
        - Audio metadata extraction with Mutagen
        - ULID-based unique file naming
        - XSS prevention and input sanitization
        - Perspective API toxicity detection for text content
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "tracks"
