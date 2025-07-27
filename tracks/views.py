from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from .models import Track
from .forms import TrackUploadForm

# Create your views here.

@login_required
def track_feed(request):
    """
    Display the main track feed for authenticated users.
    
    This view serves as the community homepage, showing all uploaded tracks
    in reverse chronological order. Only authenticated users can access this view.
    
    Args:
        request: HttpRequest object
        
    Returns:
        HttpResponse: Rendered track feed template
        
    Template: tracks/feed.html
    """
    tracks = Track.objects.all()[:5]  # Get latest 5 tracks
    return render(request, 'tracks/feed.html', {'tracks': tracks})

@login_required
def track_detail(request, slug):
    """
    Display individual track page
    """
    track = get_object_or_404(Track, slug=slug)
    return render(request, 'tracks/track_detail.html', {'track': track})

@login_required
def track_upload(request):
    """Handle modal form submission"""
    if request.method == 'POST':
        # Extract form data
        title = request.POST.get('title')
        description = request.POST.get('description')
        audio_file = request.FILES.get('audio_file')
        track_image = request.FILES.get('track_image')
        
        # Create track
        if title and audio_file:
            track = Track.objects.create(
                user=request.user,
                title=title,
                description=description,
                audio_file=audio_file,
                track_image=track_image
            )
            messages.success(request, f'Track "{track.title}" uploaded successfully!')
        else:
            messages.error(request, 'Title and audio file are required.')
    
    return redirect('track_feed')


@login_required
def track_edit(request, slug):
    """Edit an existing track."""
    track = get_object_or_404(Track, slug=slug)
    
    if track.user != request.user:
        raise Http404("Track not found")
    
    if request.method == 'POST':
        # Create form with instance but don't require files
        form = TrackUploadForm(request.POST, request.FILES, instance=track)
        
        if form.is_valid():
            updated_track = form.save(commit=False)
            
            # Keep existing files if no new ones uploaded
            if 'audio_file' not in request.FILES:
                updated_track.audio_file = track.audio_file
            
            if 'track_image' not in request.FILES:
                updated_track.track_image = track.track_image
                
            updated_track.save()
            messages.success(request, f'Track "{track.title}" updated successfully!')
            return redirect('track_detail', slug=track.slug)
    else:
        form = TrackUploadForm(instance=track)
    
    return render(request, 'tracks/edit_track.html', {
        'form': form,
        'track': track
    })



@login_required
def track_delete(request, slug):
    """
    Delete an existing track.
    
    Only accepts POST requests from the confirmation modal.
    Redirects back to track feed after successful deletion.
    """
    track = get_object_or_404(Track, slug=slug)
    
    # Check if user owns this track
    if track.user != request.user:
        raise Http404("Track not found")
    
    # Only allow POST (from modal form)
    if request.method == 'POST':
        track_title = track.title
        track.delete()
        messages.success(request, f'Track "{track_title}" deleted successfully!')
        return redirect('track_feed')
    
    # If not POST, redirect to track detail
    return redirect('track_detail', slug=slug)