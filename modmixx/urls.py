"""
URL configuration for modmixx project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Django admin interface
    path("admin/", admin.site.urls),
    # Core app - home, about, login redirects
    path("", include("core.urls")),
    # User authentication and profiles
    path("", include("accounts.urls")),
    # Django Allauth authentication (login, signup, social auth)
    path("", include("allauth.urls")),
    # Music track management and discovery
    path("tracks/", include("tracks.urls")),
    # Comment system with threading support
    path(
        "comments/",
        include(("comments.urls", "comments"), namespace="comments"),
    ),
    # Contact form and admin communication
    path("contact/", include("contact.urls")),
]
