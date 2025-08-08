from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

# create your views here.
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email to site admin
            send_mail(
                subject=f"Contact Us: {form.cleaned_data['name']}",
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=[settings.DEFAULT_FROM_EMAIL], # Site admin email
            )
            # plan to send confirmation email to user to go here
            # Generic 'we'll get back to you soon' message
            return render(request, "contact/contact_success.html")
    else:
        form = ContactForm()
    return render(request, "contact/contact.html", {"form": form})

def contact_success(request):
    return render(request, "contact/contact_success.html")