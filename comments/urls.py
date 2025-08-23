from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.post_comment, name="post_comment"),
    path("edit/<int:comment_id>/", views.comment_edit, name="comment_edit"),
    path(
        "delete/<int:comment_id>/", views.comment_delete, name="comment_delete"
    ),
]
