from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings

# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom manager for the User model.
    Handles user creation and normalization.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses email as the unique identifier.
    
    Fields:
        email: Unique email address for the user.
        first_name: User's first name.
        last_name: User's last name.
        is_active: Indicates if the user account is active.
        is_staff: Indicates if the user can access the admin site.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
    Stores information for a user profile.

    Fields:
        user: Link to the Django User model.
        username: Optional unique username for the profile.
        display_name: Optional custom name for the profile.
        bio: Optional user biography.
        pronouns: User-selected pronouns (dropdown choices).
        profile_picture: Optional profile image.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    username = models.SlugField(
        max_length=30, 
        unique=True, 
        help_text="Your unique profile URL (no spaces, letters/numbers only)"
    )
    display_name = models.CharField(
        max_length=50,
        blank=True,
        null=True, 
        help_text="Your name as shown to others (can have spaces)"
    )
    bio = models.TextField(blank=True, null=True)
    PRONOUN_CHOICES = [
        ('he/him', 'He/Him'),
        ('she/her', 'She/Her'),
        ('they/them', 'They/Them'),
        ('don\'t specify', 'Don\'t Specify'),
        ('other', 'Other'),  
    ]
    pronouns = models.CharField(max_length=50, choices=PRONOUN_CHOICES, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.username or self.user.email}'s Profile"