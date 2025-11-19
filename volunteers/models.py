from django.db import models
from django.contrib.auth import get_user_model
from crisis.models import CrisisPost

User = get_user_model()

class VolunteerApplication(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="volunteer_applications")
    crisis_post = models.ForeignKey(CrisisPost, on_delete=models.CASCADE, related_name="volunteers")
    message = models.TextField(blank=True, null=True)  # NEW: Why they want to volunteer
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "crisis_post")
        ordering = ['-applied_at']  # NEW: Latest first

    def __str__(self):
        return f"{self.user.username} - {self.crisis_post.title} ({self.status})"
    
    # NEW: Properties for easy access
    @property
    def volunteer_name(self):
        return self.user.username
    
    @property
    def crisis_title(self):
        return self.crisis_post.title