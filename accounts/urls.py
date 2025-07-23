from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html', http_method_names=['get', 'post']), name='logout'),
    path('login-redirect/', views.login_redirect, name='login_redirect'),
    path('profile/setup/', views.profile_setup, name='profile_setup'),
    path('profile/', views.profile_detail, name='profile_detail'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<slug:username>/', views.public_profile, name='public_profile'),  # Handles both user profile and public profile view
]