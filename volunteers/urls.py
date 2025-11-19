from django.urls import path
from .views import (
    ApplyVolunteerView, 
    UserVolunteerApplicationsView, 
    CrisisVolunteersListView,
    ApproveVolunteerView,
    RejectVolunteerView
)

urlpatterns = [
    path("apply/", ApplyVolunteerView.as_view(), name="apply_volunteer"),
    path("my-applications/", UserVolunteerApplicationsView.as_view(), name="my_volunteer_applications"),
    path("crisis/<int:crisis_id>/", CrisisVolunteersListView.as_view(), name="crisis_volunteers"),
    path("<int:pk>/approve/", ApproveVolunteerView.as_view(), name="approve_volunteer"),
    path("<int:pk>/reject/", RejectVolunteerView.as_view(), name="reject_volunteer"),
]