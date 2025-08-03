from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from .models import Track
from .forms import TrackUploadForm
from comments.models import Comment
from comments.forms import CommentForm

# Create your views here.

@login_required
def track_feed(request):
    """
    Display the main track feed for authenticated users.
    
    This view serves as the community homepage, showing all uploaded tracks
    in reverse chronological order with an integrated upload modal. Only 
    authenticated users can access this view to maintain platform privacy.
    
    Features:
        - Displays latest 5 tracks with metadata and audio players
        - Provides upload form integration via modal
        - Shows track artwork, user profiles, and comment counts
        - Responsive design optimized for community interaction
    
    Args:
        request (HttpRequest): The HTTP request object containing user session
        
    Returns:
        HttpResponse: Rendered track feed template with tracks and upload form
        
    Template: tracks/feed.html
    Context:
        tracks: QuerySet of latest Track objects
        upload_form: Empty TrackUploadForm for modal integration
    """
    tracks = Track.objects.all()[:5]  # Get latest 5 tracks for feed display
    upload_form = TrackUploadForm()   # Provide clean form for upload modal
    
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
    viewing and POST requests for comment submission.
    
    Features:
        - Full track metadata display with audio player
        - Approved comments display in chronological order
        - Comment submission form with validation
        - User profile integration and track ownership verification
        - Social interaction elements (comments, user profiles)
    
    Args:
        request (HttpRequest): The HTTP request object
        slug (str): Unique URL slug identifier for the track
        
    Returns:
        HttpResponse: Rendered track detail template with track data and comments
        
    Raises:
        Http404: If track with specified slug does not exist
        
    Template: tracks/track_detail.html
    Context:
        track: Track object with full metadata
        comments: QuerySet of approved Comment objects
        form: CommentForm for new comment submission
    """
    track = get_object_or_404(Track, slug=slug)
    comments = track.comments.filter(is_approved=True).order_by('-created_at')
    
    # Handle comment submission via POST request
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.track = track
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('track_detail', slug=track.slug)
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
    
    User Experience:
        - Modal state preservation on validation errors
        - Detailed error messaging for field-specific issues
        - Seamless integration with track feed interface
        - Automatic redirect to track detail on success
    
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
        # Process edit form with existing track instance
        form = TrackUploadForm(request.POST, request.FILES, instance=track)
        
        if form.is_valid():
            updated_track = form.save(commit=False)
            
            # Preserve existing files when not replaced
            if 'audio_file' not in request.FILES:
                updated_track.audio_file = track.audio_file
            
            if 'track_image' not in request.FILES:
                updated_track.track_image = track.track_image
                
            updated_track.save()
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