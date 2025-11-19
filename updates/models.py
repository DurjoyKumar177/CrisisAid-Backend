from django.db import models
from django.conf import settings
from crisis.models import CrisisPost

USER = settings.AUTH_USER_MODEL

class CrisisUpdate(models.Model):
    crisis_post = models.ForeignKey(CrisisPost, on_delete=models.CASCADE, related_name="updates")
    created_by = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="crisis_updates")
    title = models.CharField(max_length=200)
    description = models.TextField()
    update_image = models.ImageField(upload_to="update_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']  # Newest first
        verbose_name = "Crisis Update"
        verbose_name_plural = "Crisis Updates"
    
    def __str__(self):
        return f"{self.title} - {self.crisis_post.title}"
    
    @property
    def creator_name(self):
        return self.created_by.username
    
    @property
    def creator_email(self):
        return self.created_by.email
    
    @property
    def total_comments(self):
        return self.comments.count()


class Comment(models.Model):
    update = models.ForeignKey(CrisisUpdate, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']  # Newest first
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.update.title}"
    
    @property
    def commenter_name(self):
        return self.user.username