from django import forms

class ContactForm(forms.Form):
    """Form for users to contact site administrators."""
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    website = forms.CharField(required=False, widget=forms.HiddenInput)  # Honeypot field to catch spam bots

    def clean_website(self):
        data = self.cleaned_data['website']
        if data:
            raise forms.ValidationError("Spam detected.")
        return data



