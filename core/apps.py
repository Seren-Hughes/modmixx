from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Configuration for the core Django app.

    Provides central utilities, routing, and shared functionality
    for the modmixx platform. Contains no models - serves as a
    utility app for common features used across other apps.

    Features:
        - Authentication-based home page routing
        - Google Perspective API toxicity detection utilities
        - Static pages (about, terms, etc.)
        - Community-focused "sheltered" experience routing
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
