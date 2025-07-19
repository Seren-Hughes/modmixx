from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Profile(models.Model):
    """
    Stores information for a user profile.

    Fields:
        user: Link to the Django User model.
        display_name: Optional custom name for the profile.
        bio: Optional user biography.
        pronouns: User-selected pronouns (dropdown choices).
        profile_picture: Optional profile image.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=150, blank=True, null=True)
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
        return f"{self.user.username}'s Profile"