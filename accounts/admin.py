from django.contrib import admin
from .models import Profile, CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "username", "display_name", "moderation_status") 
    list_filter = ("moderation_status",)  
    search_fields = ("user__username", "username", "display_name")
    readonly_fields = ("moderation_labels", "moderated_at")
    actions = ["rescan_moderation"]

    @admin.action(description="Re-scan profile picture moderation")
    def rescan_moderation(self, request, queryset):
        from django.utils import timezone
        from tracks.services.moderation import scan_image_bytes
        
        updated = 0
        for profile in queryset:
            if not profile.profile_picture:
                continue
            
            f = profile.profile_picture.open("rb") # f = opens image file object in binary 'read mode'
            try:
                allowed, labels, failed = scan_image_bytes(f.read()) # gets the raw bytes
                if failed:
                    profile.moderation_status = "PENDING"
                    profile.moderation_labels = None
                else:
                    profile.moderation_status = "APPROVED" if allowed else "REJECTED"
                    profile.moderation_labels = labels
            except Exception:
                profile.moderation_status = "PENDING"
                profile.moderation_labels = None
            finally:
                f.close()
            
            profile.moderated_at = timezone.now()
            profile.save(update_fields=["moderation_status", "moderation_labels", "moderated_at"])
            updated += 1
        
        self.message_user(request, f"Re-scanned {updated} profile(s).")


