from django.contrib import admin
from .models import ContactMessage


# Register your models here.
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin interface for ContactMessage model with response workflow.

    Provides admin with tools to manage and respond
    to contact form submissions. Includes filtering and search for
    response tracking.

    Features:
        - List view showing key message details and response status
        - Search across all text fields for quick message lookup
        - Filtering by response status and submission date
        - Read-only timestamp fields to preserve audit trail
    """

    list_display = ("name", "email", "subject", "created_at", "responded")
    search_fields = ("name", "email", "subject", "message")
    list_filter = ("responded", "created_at")
    readonly_fields = ("created_at",)
