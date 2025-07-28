from django.shortcuts import render, get_object_or_404, redirect
from .models import Track
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def track_detail(request, slug):
    track = get_object_or_404(Track, slug=slug)
    comments = track.comments.filter(is_approved=True).order_by('-created_at')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.track = track
            comment.save()
            return redirect('track_detail', slug=track.slug)
    else:
        form = CommentForm()
    
    return render(request, 'tracks/track_detail.html', {
        'track': track,
        'comments': comments,
        'form': form,  
    })