from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Track
from .models import Comment
from .forms import CommentForm
from django.template.loader import render_to_string
import logging


logger = logging.getLogger(__name__)


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
        Django get_object_or_404 and JsonResponse documentation
    """
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # AJAX: Return JSON data, no page refresh
        # - so it won't interrupt audio playback
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {
                    "success": True,
                    "content": comment.content,
                    # Format date for display
                    # Reference: Python strftime documentation
                    "updated_at": comment.updated_at.strftime(
                        "%b %d, %Y %I:%M %p"
                    ),
                }
            )
        else:
            return JsonResponse({"success": False, "errors": form.errors})

    # fallback: redirect/reload page
    return redirect("track_detail", slug=comment.track.slug)


@login_required
@require_POST
def comment_delete(request, comment_id):
    """
    Delete a comment: soft delete if has replies, hard delete if no replies.
    Clean up soft-deleted parents recursively when all replies are gone.
    """
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    track_slug = comment.track.slug

    # Check if this comment has replies
    has_replies = comment.replies.exists()

    if has_replies:
        # Soft delete: mark as deleted but keep replies visible
        comment.deleted = True
        comment.save()
        delete_type = "soft"
        parent_cleanup = None
    else:
        # Hard delete: remove completely if no replies
        parent_comment = comment.parent
        comment.delete()
        delete_type = "hard"

        # Recursive cleanup of soft-deleted parents
        parent_cleanup = []
        current_parent = parent_comment

        while current_parent and current_parent.deleted:
            # If parent is soft-deleted and has no more replies, remove it too
            if not current_parent.replies.exists():
                parent_id = current_parent.id
                next_parent = current_parent.parent
                current_parent.delete()
                parent_cleanup.append(parent_id)
                current_parent = next_parent
            else:
                # Parent still has other replies, stop cleanup
                break

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {
                "success": True,
                "delete_type": delete_type,
                # Include parent comment ID list to remove
                "parent_cleanup": parent_cleanup,
            }
        )

    return redirect("track_detail", slug=track_slug)


@login_required
@require_POST
def post_comment(request):
    """
    Create a new comment or reply to an existing comment.

    Handles both top-level comments and threaded replies with AJAX support.
    Validates content via Perspective API before saving.

    Args:
        request: HttpRequest containing comment form data

    POST Parameters:
        track: Track ID to comment on
        content: Comment text content
        parent: Optional parent comment ID for replies

    Returns:
        JsonResponse: For AJAX requests with rendered comment HTML
        HttpResponseRedirect: For regular form submissions

    Content Moderation:
        - Automatic toxicity detection via Perspective API
        - Comments blocked if toxicity score > 0.7
        - Graceful fallback if moderation service unavailable
    """
    form = CommentForm(request.POST)
    if form.is_valid():
        track_id = request.POST.get("track")
        track = get_object_or_404(Track, id=track_id)
        comment = form.save(commit=False)
        comment.track = track
        comment.user = request.user
        comment.save()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            html = render_to_string(
                "comments/_comment.html",
                {
                    "comment": comment,
                    "level": 0,
                    "user": request.user,
                    "track": track,
                },
                request=request,
            )
            return JsonResponse({"success": True, "comment_html": html})

        return redirect("track_detail", slug=track.slug)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {"success": False, "errors": form.errors}, status=400
        )

    # Fallback redirect
    track_id = request.POST.get("track")
    if track_id:
        track = get_object_or_404(Track, id=track_id)
        return redirect("track_detail", slug=track.slug)
    return redirect("/")
