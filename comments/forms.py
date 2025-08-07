from django import forms
from .models import Comment
from .utils import get_toxicity_score
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

class CommentForm(forms.ModelForm):
    """
    Form for creating and editing comments with content moderation.
    Uses Google's Perspective API to detect and block toxic content.
    """
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

    def clean_content(self):
        """
        Validate comment content for toxicity using Perspective API.
        Blocks comments with toxicity score above 0.7 threshold.
        """
        content = self.cleaned_data.get('content')
        if content:
            try:
                # Check content toxicity using Perspective API
                toxicity = get_toxicity_score(content)
                if toxicity > 0.7:
                    raise ValidationError("Your comment may contain toxic language. Please revise.")
            except ValidationError:
                # Re-raise validation errors (don't suppress toxicity blocks)
                raise
            except Exception as e:
                # Log API errors but allow comment if moderation service fails
                print(f"Perspective API error: {e}")
                pass
        return content

def post_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('somewhere')
        # If not valid, fall through to re-render the form with errors
    else:
        form = CommentForm()
    return render(request, 'comments/comment_form.html', {'form': form})

@login_required
@require_POST
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    form = CommentForm(request.POST, instance=comment)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'content': comment.content,
                'updated_at': comment.updated_at.strftime('%b %d, %Y %I:%M %p')
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        if form.is_valid():
            form.save()
            return redirect('track_detail', slug=comment.track.slug)
        else:
            # Re-render the form with errors
            return render(request, 'comments/comment_form.html', {'form': form, 'comment': comment})