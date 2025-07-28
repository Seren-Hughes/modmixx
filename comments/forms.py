from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
    'content': forms.Textarea(attrs={
        'rows': 2,
        'placeholder': 'Comment prompt…',
        'class': 'form-control',
        'style': 'resize:vertical;'
    }),
}