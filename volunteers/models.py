from django.db import models
from django.contrib.auth import get_user_model
from crisis.models import CrisisPost # Assuming Crisis app has a CrisisPost model

User = get_user_model()

class VolunteerApplication(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="volunteer_applications")
    crisis_post = models.ForeignKey(CrisisPost, on_delete=models.CASCADE, related_name="volunteers")
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    class Meta:
        unique_together = ("user", "crisis_post")  # prevent duplicate applications

    def __str__(self):
        return f"{self.user.username} - {self.crisis_post.title} ({self.status})"
