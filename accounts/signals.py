from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.signals import (
    social_account_added,
    social_account_removed,
)
from django.core.mail import send_mail
from django.dispatch import receiver


@receiver(user_signed_up)
def send_welcome_email_on_social_signup(sender, request, user, **kwargs):
    """
    Sends welcome email when users sign up via Google OAuth.

    Note: This fires when user actually completes the signup form, not just
    when they click the Google button. Fixed the timing issue where emails
    were being sent too early (when signup page loaded vs form submitted).
    """
    try:
        # Check if this was a Google signup by looking for social account
        social_account = SocialAccount.objects.get(  # noqa: F841
            user=user, provider="google"
        )
        user_email = user.email

        if user_email:
            send_mail(
                subject="Welcome to modmixx 🎉",
                message=(
                    "Thanks for signing up to modmixx with Google!\n\n"
                    "We're thrilled to have you in our collaborative "
                    "music community. Dive in, explore, and start creating!"
                ),
                from_email="modmixx <modmixx.platform@gmail.com>",
                recipient_list=[user_email],
                fail_silently=True,
            )
    except SocialAccount.DoesNotExist:
        # Not a social signup, skip sending email
        pass
    except Exception as e:
        print(f"Failed to send Google signup welcome email: {e}")


@receiver(social_account_added)
def send_connection_confirmation_email(sender, request, sociallogin, **kwargs):
    """
    Sends confirmation email when existing users connect their Gmail account.

    Important: Email goes to the newly connected Gmail address,
    not the original account email, since they might be different.
    This way the person who owns the Gmail gets notified if someone
    connects their account to modmixx.

    Had to use sociallogin.user.email instead of .username because
    my CustomUser model doesn't have a username field - it uses email
    as the identifier.
    """
    user = sociallogin.user
    provider = sociallogin.account.provider

    # Only send for Google connections
    if provider == "google":
        try:
            # Get the Gmail address from the OAuth data
            connected_gmail = sociallogin.account.extra_data.get("email")

            if connected_gmail:
                # Get user's display name safely (with fallback)
                display_name = (
                    getattr(user.profile, "display_name", None)
                    if hasattr(user, "profile")
                    else None
                )
                if not display_name:
                    # Use part before @ as fallback if no display name set
                    display_name = user.email.split("@")[0]

                send_mail(
                    subject="Gmail Connected to modmixx",
                    message=(
                        f"Hey {display_name}!\n\n"
                        f"Your Gmail account ({connected_gmail}) "
                        f"has been successfully connected "
                        f"to your modmixx account ({user.email}).\n\n"
                        "You can now sign in using either email address.\n\n"
                        "Keep creating!\n"
                        "- The modmixx team"
                    ),
                    from_email="modmixx <modmixx.platform@gmail.com>",
                    recipient_list=[
                        connected_gmail
                    ],  # Send to Gmail, not original email
                    fail_silently=False,
                )

        except Exception as e:
            print(f"Failed to send Gmail connection confirmation email: {e}")


@receiver(social_account_removed)
def send_disconnection_email(sender, request, socialaccount, **kwargs):
    """
    Sends confirmation email when users disconnect their Gmail account.

    This is important for security - if someone unauthorized disconnects
    a Gmail account, the owner of that Gmail address gets notified. Same
    principle as the connection email but in reverse.

    Note: Using socialaccount parameter (not sociallogin like in connection)
    because the disconnection signal passes the account object directly.
    """
    # Only handle Google account disconnections
    if socialaccount.provider == "google":
        try:
            # Get the Gmail that was just disconnected
            disconnected_gmail = socialaccount.extra_data.get("email")

            if disconnected_gmail:
                send_mail(
                    subject="Gmail Account Disconnected from modmixx",
                    message=(
                        "Your Gmail account has been disconnected "
                        "from modmixx.\n\n"
                        "- The modmixx team"
                    ),
                    from_email="modmixx <modmixx.platform@gmail.com>",
                    recipient_list=[
                        disconnected_gmail
                    ],  # Send to the disconnected Gmail
                    fail_silently=False,
                )
        except Exception as e:
            print(f"Failed to send Gmail disconnection email: {e}")
