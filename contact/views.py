from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import ContactMessage


# create your views here.
def contact(request):
    """
    Handle contact form submission and email processing.

    Processes GET requests by displaying the contact form and POST requests
    by validating, sending emails, and saving messages to database.

    GET Request:
        Renders contact form for user input

    POST Request:
        - Validates form data including honeypot spam detection
        - Sends notification email to site administrators
        - Saves message to ContactMessage model for tracking
        - Sends confirmation email to user
        - Renders success page on completion

    Email Flow:
        1. Admin notification with user's message content
        2. User confirmation acknowledging receipt
        3. Graceful error handling if email service fails

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse: Rendered contact form or success page

    Security Features:
        - Honeypot field spam detection
        - Email header validation
        - Form field sanitization
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                # Send email to site admin
                send_mail(
                    subject=f"Contact Us: {form.cleaned_data['name']}",
                    message=form.cleaned_data["message"],
                    from_email=form.cleaned_data["email"],
                    recipient_list=[
                        settings.DEFAULT_FROM_EMAIL
                    ],  # Site admin email
                    fail_silently=False,
                )
            except Exception:
                form.add_error(
                    None,
                    "There was a problem sending your message. "
                    "Please try again later.",
                )
            else:
                # Save message, redirect to success, etc.
                ContactMessage.objects.create(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"],
                    subject=form.cleaned_data["subject"],
                    message=form.cleaned_data["message"],
                )
                # Send confirmation email to user
                send_mail(
                    subject="We've received your message",
                    message="Thank you for contacting modmixx! "
                    "The team will get back to you soon.",
                    from_email="modmixx <modmixx.platform@gmail.com>",
                    recipient_list=[form.cleaned_data["email"]],
                    fail_silently=True,
                )
                # Confirmation
                return render(request, "contact/contact_success.html")
    else:
        form = ContactForm()
    return render(request, "contact/contact.html", {"form": form})


def contact_success(request):
    """
    Display contact form submission success message.

    Simple view to confirm successful contact form submission.
    Accessed after successful form processing or direct URL.

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse: Rendered success confirmation page
    """
    return render(request, "contact/contact_success.html")
