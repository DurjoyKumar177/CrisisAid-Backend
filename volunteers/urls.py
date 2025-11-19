from django.urls import path
from .views import ApplyVolunteerView, UserVolunteerApplicationsView, ApproveRejectVolunteerView

urlpatterns = [
    path("apply/", ApplyVolunteerView.as_view(), name="apply_volunteer"),
    path("my-applications/", UserVolunteerApplicationsView.as_view(), name="my_volunteer_applications"),
    path("approve-reject/<int:pk>/", ApproveRejectVolunteerView.as_view(), name="approve_reject_volunteer"),
]
