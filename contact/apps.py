from django.apps import AppConfig


class ContactConfig(AppConfig):
    """
    Configuration for the contact Django app.

    Handles contact form submissions with email notifications and
    admin response workflow. Includes spam detection via honeypot
    field and dual email system for both admin alerts and user
    confirmations.

    Features:
        - Contact form with spam protection (honeypot field)
        - Dual email notifications (admin alert + user confirmation)
        - Message storage and admin response tracking
        - Customer service workflow with response status
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "contact"
