from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Track

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
    """
    Upload a new track - placeholder for now
    """
    return render(request, 'tracks/track_upload.html')