from django.urls import path
from . import views

# URL patterns for the tracks app
# Currently implements basic feed structure for Iteration 2 development
urlpatterns = [
    path('', views.track_feed, name='track_feed'), # Main track feed
]