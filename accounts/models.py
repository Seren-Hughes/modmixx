from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
    TemporaryUploadedFile,
)
from django.db import models

# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the User model.
    Handles user creation and normalization.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses email as the unique identifier.

    Replaces Django's default username-based authentication with
    email-based authentication for better user experience.

    Fields:
        email: Unique email address for authentication and identification
        is_active: Boolean indicating if the user account is active
        is_staff: Boolean indicating if the user can access admin site

    Related Models:
        Profile: OneToOneField relationship (user.profile)
            - created automatically via signals
        Track: ForeignKey relationship via Profile (user.profile.tracks)

    Manager:
        CustomUserManager: Handles email-based user creation and normalization

    Authentication:
        Uses email instead of username for login
        USERNAME_FIELD = "email"
        No required fields beyond email and password
    """

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
    User profile information with content moderation capabilities.

    Each CustomUser automatically gets one Profile created via post_save
    signals upon registration. Contains public profile information and
    handles profile picture moderation through AWS Rekognition.

    Fields:
        user: OneToOneField to CustomUser (primary relationship)
        username: Unique slug for profile URLs (/profile/{username}/)
        display_name: Optional public display name shown to other users
        bio: Optional biography text (max 500 chars, XSS protected in forms)
        pronouns: User's preferred pronouns (free text, max 50 chars)
        profile_picture: Optional profile image (uploaded to S3, moderated)
        moderation_status: PENDING/APPROVED/REJECTED status for profile images
        moderation_labels: AWS Rekognition labels if image rejected
        moderated_at: Timestamp of last moderation check

    Related Models:
        CustomUser: OneToOneField (profile.user)
        Track: ForeignKey relationship via user (user.tracks.all())

    URL Pattern:
        Accessible at /profile/{username}/

    Content Moderation:
        - New profile images automatically scanned via AWS Rekognition
        - NSFW/inappropriate content automatically rejected
        - Manual re-scanning available in Django admin
        - Toxicity checking on text fields via Perspective API

    File Management:
        - Automatic cleanup of old profile pictures on replacement
        - ULID-based unique filenames for storage security
        - S3 storage with automatic deletion of unused files
        - Custom save() method handles file cleanup

    Security Features:
        - XSS protection in form validation
        - HTML tag stripping in text fields
        - Dangerous pattern detection (javascript:, onclick=, etc.)
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    username = models.SlugField(
        max_length=30,
        unique=True,
        help_text="Your unique profile URL (no spaces, letters/numbers only)",
    )
    display_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Your name as shown to others (can have spaces)",
    )
    bio = models.TextField(blank=True, null=True)
    pronouns = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g., she/her, they/them, he/they, xe/xir",
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )

    MOD_STATUS = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )
    moderation_status = models.CharField(
        max_length=9, choices=MOD_STATUS, default="PENDING"
    )
    moderation_labels = models.JSONField(blank=True, null=True)
    moderated_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Custom save method to handle profile picture cleanup.

        - If the profile picture is replaced or cleared,
          delete the old file from storage (S3).
        - Only deletes the old file if:
            * The clear checkbox was checked (profile_picture is now None)
            * A new file was uploaded (profile_picture is
            * a new InMemoryUploadedFile or TemporaryUploadedFile)
        """
        try:
            old = Profile.objects.get(pk=self.pk)
        except Profile.DoesNotExist:
            old = None

        super().save(*args, **kwargs)

        # Delete the old profile picture if it was replaced or cleared
        if (
            old
            and old.profile_picture
            and old.profile_picture != self.profile_picture
        ):
            if not self.profile_picture:
                # User cleared the image via the clear checkbox
                old.profile_picture.delete(save=False)
            elif isinstance(
                self.profile_picture.file,
                (InMemoryUploadedFile, TemporaryUploadedFile),
            ):
                # User uploaded a new image, so remove the old file
                old.profile_picture.delete(save=False)

    def __str__(self):
        return f"{self.username or self.user.email}'s Profile"
