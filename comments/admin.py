from django.contrib import admin
from .models import Comment

# Register your models here.
admin.site.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'created_at', 'is_approved', 'needs_review')
    list_filter = ('is_approved', 'needs_review')
    search_fields = ('content',)