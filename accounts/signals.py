from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login
from django.core.mail import send_mail

@receiver(pre_social_login)
def send_welcome_email_on_social_signup(sender, request, sociallogin, **kwargs):
    """
    Send welcome email when user signs up via Google OAuth.
    
    Only triggers for new users, not existing users connecting accounts.
    """
    # Only send email for new users (not existing users connecting accounts)
    if sociallogin.is_existing:
        return
    
    # Get user email from social account data
    user_email = sociallogin.account.extra_data.get('email')
    
    if user_email:
        try:
            send_mail(
                subject="Welcome to modmixx 🎉",
                message=(
                    "Thanks for signing up to modmixx with Google!\n\n"
                    "We're thrilled to have you in our collaborative music community. "
                    "Dive in, explore, and start creating!"
                ),
                from_email="modmixx <modmixx.platform@gmail.com>",
                recipient_list=[user_email],
                fail_silently=True,
            )
        except Exception as e:
            # Log error but don't break the signup process
            print(f"Failed to send Google signup email: {e}")