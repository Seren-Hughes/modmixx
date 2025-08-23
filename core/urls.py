from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path(
        "test-500/", views.test_500, name="test_500"
    ),  # Test 500 error view - temporary delete when done
]
