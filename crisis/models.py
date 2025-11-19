from django.db import models
from django.conf import settings

USER = settings.AUTH_USER_MODEL

class CrisisPost(models.Model):
    POST_TYPES = (
        ("national", "National-Level"),
        ("district", "District-Level"),
        ("individual", "Individual-Level"),
    )
    
    STATUS_CHOICES = (
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPES)
    location = models.CharField(max_length=200, blank=True, null=True)  # NEW: Add location
    owner = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="crisis_posts")
    banner_image = models.ImageField(upload_to="crisis_banners/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']  # NEW: Default ordering
    
    def __str__(self):
        return f"{self.title} ({self.post_type})"
    
    # NEW: Properties to easily access owner info
    @property
    def owner_name(self):
        return self.owner.username
    
    @property
    def owner_email(self):
        return self.owner.email


class PostSection(models.Model):
    SECTION_CHOICES = (
        ("shelter", "Shelter"),
        ("resources", "Resources/Goods"),
        ("fund", "Fund Collection"),
        ("hotline", "Hotline Updates"),
        ("distribution", "Distribution History"),
        ("updates", "Crisis Updates"),
    )
    
    post = models.ForeignKey(CrisisPost, on_delete=models.CASCADE, related_name="sections")
    section_type = models.CharField(max_length=20, choices=SECTION_CHOICES)
    content = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_sections")  # NEW: Track creator
    created_at = models.DateTimeField(auto_now_add=True)  # NEW

    def __str__(self):
        return f"{self.post.title} - {self.section_type}"
    
    # NEW: Property to get creator name
    @property
    def creator_name(self):
        return self.created_by.username if self.created_by else "Unknown"