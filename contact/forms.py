from django import forms

class ContactForm(forms.Form):
    """Form for users to contact site administrators."""
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)