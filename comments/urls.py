from django.urls import path
from . import views

urlpatterns = [
    path('edit/<int:comment_id>/', views.comment_edit, name='comment_edit'),
    path('delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
]