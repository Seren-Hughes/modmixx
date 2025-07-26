from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
        tags = request.POST.get('tags', '')
        audio_file = request.FILES.get('audio_file')
        track_image = request.FILES.get('track_image')
        
        # Create track
        if title and audio_file:
            track = Track.objects.create(
                user=request.user,
                title=title,
                description=description,
                tags=tags,
                audio_file=audio_file,
                track_image=track_image
            )
            messages.success(request, f'Track "{track.title}" uploaded successfully!')
        else:
            messages.error(request, 'Title and audio file are required.')
    
    return redirect('track_feed')