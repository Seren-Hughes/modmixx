from django.contrib import admin
from django.utils import timezone
from .models import Track
from .services.moderation import scan_image_bytes


# Register your models here.
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "created_at", "moderation_status"]
    list_filter = ["moderation_status", "created_at"]
    search_fields = ["title", "description", "user__username"]
    readonly_fields = ["moderation_labels", "moderated_at"]
    ordering = ["-created_at"]
    actions = ["rescan_moderation"]

    @admin.action(description="Re-scan image moderation")
    def rescan_moderation(self, request, queryset):
        """
        Bulk action to re-scan track images using AWS Rekognition.
        Updates moderation status and labels for selected tracks.
        """
        updated = 0
        for track in queryset:
            if not track.track_image:
                continue

            f = track.track_image.open("rb")
            try:
                allowed, labels, failed = scan_image_bytes(f.read())
            except Exception:
                # Fail-open on admin action: mark pending
                track.moderation_status = "PENDING"
                track.moderation_labels = None
            else:
                if failed:
                    track.moderation_status = "PENDING"
                    track.moderation_labels = None
                else:
                    track.moderation_status = (
                        "APPROVED" if allowed else "REJECTED"
                    )
                    track.moderation_labels = labels
            finally:
                f.close()

            track.moderated_at = timezone.now()
            track.save(
                update_fields=[
                    "moderation_status",
                    "moderation_labels",
                    "moderated_at",
                ]
            )
            updated += 1

        self.message_user(request, f"Re-scanned {updated} track(s).")
