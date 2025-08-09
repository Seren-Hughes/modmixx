from django.urls import path
from . import views

# URL patterns for the tracks app
urlpatterns = [
    path('', views.track_feed, name='track_feed'), # Main track feed
    path('upload/', views.track_upload, name='track_upload'),
    path('<slug:slug>/edit/', views.track_edit, name='track_edit'),
    path('<slug:slug>/delete/', views.track_delete, name='track_delete'),
    path('<slug:slug>/', views.track_detail, name='track_detail'),
    path('feed-api/', views.track_feed_api, name='track_feed_api'), # API endpoint for track feed
]