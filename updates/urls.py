from django.urls import path
from .views import (
    CreateCrisisUpdateView,
    CrisisUpdatesListView,
    CrisisUpdateDetailView,
    MyUpdatesView,
    CreateCommentView,
    UpdateCommentsListView,
    CommentDetailView,
    MyCommentsView
)

urlpatterns = [
    # Crisis Updates
    path("create/", CreateCrisisUpdateView.as_view(), name="create_crisis_update"),
    path("crisis/<int:crisis_id>/", CrisisUpdatesListView.as_view(), name="crisis_updates_list"),
    path("<int:pk>/", CrisisUpdateDetailView.as_view(), name="crisis_update_detail"),
    path("my-updates/", MyUpdatesView.as_view(), name="my_updates"),
    
    # Comments
    path("comment/create/", CreateCommentView.as_view(), name="create_comment"),
    path("<int:update_id>/comments/", UpdateCommentsListView.as_view(), name="update_comments_list"),
    path("comment/<int:pk>/", CommentDetailView.as_view(), name="comment_detail"),
    path("my-comments/", MyCommentsView.as_view(), name="my_comments"),
]