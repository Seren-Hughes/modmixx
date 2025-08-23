from django import forms
from .models import Comment
from core.utils import get_toxicity_score
from django.core.exceptions import ValidationError


class CommentForm(forms.ModelForm):
    """
    Form for creating and editing comments with content moderation.
    Uses Google's Perspective API to detect and block toxic content.
    """

    parent = forms.ModelChoiceField(
        queryset=Comment.objects.all(),
        required=False,
        widget=forms.HiddenInput,
    )

    class Meta:
        model = Comment
        fields = ["content", "parent"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "Comment prompt…",
                    "class": "form-control",
                    "style": "resize:vertical;",
                }
            ),
        }

    def clean_content(self):
        """
        Validate comment content for toxicity using Perspective API.
        Blocks comments with toxicity score above 0.7 threshold.
        """
        content = self.cleaned_data.get("content")
        if content:
            try:
                # Check content toxicity using Perspective API
                toxicity = get_toxicity_score(content)
                if toxicity > 0.7:
                    raise ValidationError(
                        "Your comment may contain toxic language. "
                        "Please revise."
                    )
            except ValidationError:
                # Re-raise validation errors (don't suppress toxicity blocks)
                raise
            except Exception as e:
                # Log API errors but allow comment if moderation service fails
                print(f"Perspective API error: {e}")
                pass
        return content
