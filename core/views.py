from django.shortcuts import render


# Create your views here.
def home(request):
    """
    Handle homepage routing based on user authentication status.

    Implements a 'sheltered community' approach:
    - Authenticated users: Redirected to track feed (community content)
    - Anonymous users: Shown public landing page with signup/login options

    This creates a members-only experience where the main content is only
    visible to registered community members.

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse: Either track feed or landing page
    """
    if request.user.is_authenticated:
        from tracks.views import track_feed

        return track_feed(request)
    else:
        return render(request, "core/home.html")


def about(request):
    """About page with community guidelines and site information."""
    return render(request, "core/about.html")


# Test 500 error view Temporary - delete
def test_500(request):
    raise Exception("Test 500 error")
