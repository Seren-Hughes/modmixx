from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration for the accounts app.

    Manages user authentication and profiles with automatic
    Profile creation via signals and AWS image moderation.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        # Import signals to ensure they are registered
        # (noqa for false positive flake8 errors)
        import accounts.signals  # noqa: F401
