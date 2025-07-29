from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Track
from .models import Comment
from .forms import CommentForm


# Create your views here.
@login_required
@require_POST
def comment_edit(request, comment_id):
    """
    Edit an existing comment.
    Handles both AJAX requests and regular form submissions.
    If AJAX, returns JSON response with updated comment content.
    If regular form submission, redirects to the track detail page.

    Args:
        request: HttpRequest object
        comment_id: ID of the comment to edit
    Returns:
        HttpResponse: JSON response for AJAX, or redirect 
    Raises:
        Http404: If comment does not exist or user does not own the comment 
    References:
        - https://docs.djangoproject.com/en/5.2/topics/http/shortcuts/#get-object-or-404
        - https://docs.djangoproject.com/en/5.2/ref/request-response/#jsonresponse-objects
    """
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX: Return JSON data, no page refresh - won't interrupt audio playback
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'content': comment.content,
                'updated_at': comment.updated_at.strftime('%b %d, %Y %I:%M %p') # Format date for display - can be tweaked = https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    # fallback: redirect/reload page 
    return redirect('track_detail', slug=comment.track.slug)

@login_required
@require_POST
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    track_slug = comment.track.slug
    comment.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('track_detail', slug=track_slug)