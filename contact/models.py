from django.db import models


# Create your models here.
class ContactMessage(models.Model):
    """
    Contact form submission storage with admin workflow support.

    Stores user contact form submissions for admin review and response
    tracking. Includes spam detection via honeypot field in ContactForm.

    Fields:
        name: CharField max 100 chars (submitter's name)
        email: EmailField (submitter's email for response)
        subject: CharField max 200 chars (message subject line)
        message: TextField (main message content)
        created_at: DateTimeField auto-generated (submission timestamp)
        responded: BooleanField default False (admin response tracking)
        responded_at: DateTimeField optional (response timestamp)
        response_notes: TextField optional (admin notes for followup)

    Admin Features:
        - List view with filtering by response status and date
        - Search across name, email, subject, and message fields
        - Response tracking workflow for customer service

    Security:
        - Honeypot spam detection in ContactForm
        - Email validation and sanitization
        - Admin-only access to stored messages
    """

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)
    responded_at = models.DateTimeField(null=True, blank=True)
    response_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.subject} from {self.name} ({self.email})"
