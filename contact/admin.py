from django.contrib import admin
from .models import ContactMessage

# Register your models here.
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'responded')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('responded', 'created_at')
    readonly_fields = ('created_at',)