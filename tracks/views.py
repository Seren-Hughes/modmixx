from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from django.utils.timesince import timesince
from django.contrib import messages
from django.http import Http404
from django.db.models import Count, Q
from .models import Track
from .forms import TrackUploadForm
from comments.models import Comment
from comments.forms import CommentForm

# Create your views here.
@login_required
def track_feed(request):
    """
    Server-render (SSR) the first page (5 newest tracks).
    Only show APPROVED tracks to maintain community standards.
    """
    tracks = (
        Track.objects
        .filter(moderation_status="APPROVED")  # Only approved tracks
        .select_related('user', 'user__profile')
        .annotate(comment_count=Count('comments'))
        .order_by('-created_at')[:5]
    )
    upload_form = TrackUploadForm()
    return render(request, 'tracks/feed.html', {
        'tracks': tracks,
        'upload_form': upload_form,
    })


@login_required
def track_detail(request, slug):
    """
    Display individual track page with full details and comment functionality.
    
    This view provides comprehensive track information including audio playback,
    user comments, and interaction capabilities. Handles both GET requests for
    viewing and POST requests for comment submission with automated content moderation.
    
    Features:
        - Full track metadata display with audio player
        - Approved comments display in chronological order
        - Comment submission form with validation and toxicity detection
        - Perspective API integration for automated content moderation
        - User profile integration and track ownership verification
        - Social interaction elements (comments, user profiles)
        - Moderation-aware access (users can see own pending tracks)
    
    Content Moderation:
        - Integrates Google Perspective API for toxic language detection
        - Blocks comments with toxicity score above 0.7 threshold
        - Displays user-friendly error messages for flagged content
        - Graceful fallback if moderation API is unavailable
        - Maintains comment quality and community safety standards
        - AWS Rekognition image moderation status display
    
    Args:
        request (HttpRequest): The HTTP request object
        slug (str): Unique URL slug identifier for the track
        
    Returns:
        HttpResponse: Rendered track detail template with track data and comments
        
    Raises:
        Http404: If track with specified slug does not exist or user lacks access
        
    Template: tracks/track_detail.html
    Context:
        track: Track object with full metadata
        comments: QuerySet of approved Comment objects
        form: CommentForm for new comment submission with validation errors
    """
    # for now users can see their own tracks regardless of moderation status * clumsy needs to be fixed
    # All other users only see approved tracks
    track = get_object_or_404(
        Track.objects.select_related('user', 'user__profile'),
        Q(slug=slug) & (Q(moderation_status="APPROVED") | Q(user=request.user))
    )
    
    comments = Comment.objects.filter(track=track).order_by('-created_at')
    
    # Handle comment submission with content moderation
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Save valid comment
            comment = form.save(commit=False)
            comment.user = request.user
            comment.track = track
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('track_detail', slug=track.slug)
        else:
            # Form is invalid (e.g., toxic content detected)
            # Fall through to re-render page with validation errors
            pass
    else:
        form = CommentForm()
    
    return render(request, 'tracks/track_detail.html', {
        'track': track,
        'comments': comments,
        'form': form,
    })


@login_required
def track_upload(request):
    """
    Handle track upload with comprehensive form validation and security measures.
    
    This view processes track uploads through a modal form interface, implementing
    multiple layers of validation for security and data integrity. On validation
    errors, maintains modal state and provides detailed user feedback.
    
    Security Features:
        - XSS prevention through input validation
        - File type and size validation
        - MIME type verification
        - Filename sanitization
        - User authentication verification
        - AWS Rekognition image moderation with fail-open policy
    
    User Experience:
        - Modal state preservation on validation errors
        - Detailed error messaging for field-specific issues
        - Seamless integration with track feed interface
        - Automatic redirect to track detail on success
        - User notification for pending moderation status
    
    Args:
        request (HttpRequest): The HTTP request object with form data and files
        
    Returns:
        HttpResponse: Redirect to track detail on success, or rendered feed with errors
        
    Template: tracks/feed.html (on validation errors)
    Context (on errors):
        tracks: Latest tracks for feed display
        upload_form: Form instance with validation errors
        show_upload_modal: Boolean flag to keep modal open
    """
    if request.method == 'POST':
        form = TrackUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save track with user association
            track = form.save(commit=False)
            track.user = request.user
            track.save()
            
            # Check moderation status and provide appropriate feedback
            if track.moderation_status == "PENDING":
                messages.warning(
                    request,
                    f'Track "{track.title}" uploaded successfully! Your artwork is pending moderation and will be reviewed shortly.'
                )
            elif track.moderation_status == "REJECTED":
                messages.error(
                    request,
                    f'Track "{track.title}" was uploaded but the artwork was flagged during moderation.'
                )
            else:
                messages.success(request, f'Track "{track.title}" uploaded successfully!')
            
            return redirect('track_detail', slug=track.slug)
        else:
            # Handle validation errors with user-friendly messaging
            error_messages = {
                'audio_file': 'Please upload a valid audio file (MP3, WAV, FLAC, M4A, AAC, or OGG)',
                'track_image': 'Please upload a valid image file (JPG, PNG, or WebP)',
                'title': 'Please check your track title',
                'description': 'Please check your track description'
            }
            
            # Provide detailed error feedback for each field
            for field, errors in form.errors.items():
                field_name = error_messages.get(field, field.replace('_', ' ').title())
                for error in errors:
                    messages.error(request, f"{field_name}: {error}")
            
            # Render feed with modal state preserved for error correction
            tracks = Track.objects.all()[:5]
            return render(request, 'tracks/feed.html', {
                'tracks': tracks,
                'upload_form': form,
                'show_upload_modal': True,
            })
    
    # Redirect GET requests to main feed
    return redirect('track_feed')


@login_required
def track_edit(request, slug):
    """
    Handle track editing with file preservation and validation.
    
    This view allows track owners to modify their track metadata and optionally
    replace audio or image files. Implements ownership verification and preserves
    existing files when not replaced during editing.
    
    Features:
        - Track ownership verification for security
        - Optional file replacement (preserves existing when not uploaded)
        - Full form validation with security measures
        - Seamless user experience with pre-populated form data
        - Success messaging and proper redirects
    
    File Handling:
        - Preserves existing audio file if no new file uploaded
        - Preserves existing track image if no new image uploaded
        - Validates new files with same security measures as upload
        - Maintains file integrity throughout edit process
    
    Args:
        request (HttpRequest): The HTTP request object
        slug (str): Unique URL slug identifier for the track to edit
        
    Returns:
        HttpResponse: Rendered edit form on GET, redirect to track detail on success
        
    Raises:
        Http404: If track does not exist or user is not the owner
        
    Template: tracks/edit_track.html
    Context:
        form: TrackUploadForm instance with current track data
        track: Track object being edited
    """
    track = get_object_or_404(Track, slug=slug)
    
    # Verify track ownership for security
    if track.user != request.user:
        raise Http404("Track not found")
    
    if request.method == 'POST':
        # Store references to old files before form processing
        old_audio_file = track.audio_file if track.audio_file else None
        old_image_file = track.track_image if track.track_image else None
        
        # Process edit form with existing track instance
        form = TrackUploadForm(request.POST, request.FILES, instance=track)
        
        if form.is_valid():
            # Save the updated track
            updated_track = form.save()
            
            # Delete old audio file if a new one was uploaded
            if 'audio_file' in form.changed_data and old_audio_file:
                if old_audio_file != updated_track.audio_file:
                    old_audio_file.delete(save=False)
            
            # Delete old image file if a new one was uploaded
            if 'track_image' in form.changed_data and old_image_file:
                if old_image_file != updated_track.track_image:
                    old_image_file.delete(save=False)
            
            messages.success(request, f'Track "{track.title}" updated successfully!')
            return redirect('track_detail', slug=track.slug)
        else:
            # Handle validation errors during edit
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        # Pre-populate form with existing track data
        form = TrackUploadForm(instance=track)
    
    return render(request, 'tracks/edit_track.html', {
        'form': form,
        'track': track
    })


@login_required
def track_delete(request, slug):
    """
    Handle track deletion with ownership verification and confirmation.
    
    This view provides secure track deletion functionality, requiring POST
    requests from confirmation modals and verifying track ownership before
    allowing deletion. Implements proper cleanup and user feedback.
    
    Security Features:
        - Track ownership verification
        - POST-only deletion (prevents CSRF and accidental deletion)
        - Proper error handling and user feedback
        - Secure redirect patterns
    
    User Experience:
        - Confirmation modal integration
        - Success messaging with deleted track title
        - Proper redirect to community feed
        - Graceful handling of invalid requests
    
    Args:
        request (HttpRequest): The HTTP request object
        slug (str): Unique URL slug identifier for the track to delete
        
    Returns:
        HttpResponse: Redirect to feed on successful deletion, track detail on invalid request
        
    Raises:
        Http404: If track does not exist or user is not the owner
        
    Security Notes:
        - Only accepts POST requests from confirmation forms
        - Verifies user ownership before allowing deletion
        - Prevents unauthorized access through proper error handling
    """
    track = get_object_or_404(Track, slug=slug)
    
    # Verify track ownership for security
    if track.user != request.user:
        raise Http404("Track not found")
    
    # Only allow POST requests from confirmation modal
    if request.method == 'POST':
        track_title = track.title  # Store title before deletion for messaging
        track.delete()
        messages.success(request, f'Track "{track_title}" deleted successfully!')
        return redirect('track_feed')
    
    # Redirect invalid requests back to track detail
    return redirect('track_detail', slug=slug)

def upload_track(request):
    messages.success(request, "Track uploaded successfully!")
    return redirect('feed')



def track_feed_api(request):
    """
    JSON endpoint for infinite scroll.
    Only return APPROVED tracks.
    """
    page = int(request.GET.get('page', 1))
    tracks_qs = (
        Track.objects
        .filter(moderation_status="APPROVED")  # Only approved tracks
        .select_related('user', 'user__profile')
        .annotate(comment_count=Count('comments'))
        .order_by('-created_at')
    )
    paginator = Paginator(tracks_qs, 5)
    page_obj = paginator.get_page(page)

    items = []
    for t in page_obj:
        items.append({
            "id": t.id,
            "title": t.title,
            "slug": t.slug,
            "detail_url": reverse('track_detail', args=[t.slug]),
            "description": t.description or "",
            "created_ago": f"{timesince(t.created_at)} ago",
            "audio_url": t.audio_file.url,
            "image_url": t.track_image.url if t.track_image else None,
            "comment_count": t.comment_count,  # Annotated (no extra query)
            "profile": {
                "username": t.user.profile.username,
                # Fallback: use username if no display_name set
                "display_name": t.user.profile.display_name or t.user.profile.username,
                "url": reverse('profile', args=[t.user.profile.username]),
                "avatar": t.user.profile.profile_picture.url if t.user.profile.profile_picture else None,
            },
        })

    return JsonResponse({
        "tracks": items,
        "has_next": page_obj.has_next(),
    })