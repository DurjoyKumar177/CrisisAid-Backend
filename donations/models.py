from django.db import models
from django.conf import settings
from crisis.models import CrisisPost

USER = settings.AUTH_USER_MODEL

class DonationMoney(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ("bkash", "bKash"),
        ("nagad", "Nagad"),
        ("rocket", "Rocket"),
        ("bank", "Bank Transfer"),
        ("card", "Credit/Debit Card"),
        ("other", "Other"),
    )
    
    crisis_post = models.ForeignKey(CrisisPost, on_delete=models.CASCADE, related_name="money_donations")
    donor = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="money_donations")
    donor_name = models.CharField(max_length=100, blank=True, null=True)  # For anonymous/guest donors
    donor_email = models.EmailField(blank=True, null=True)
    donor_phone = models.CharField(max_length=20, blank=True, null=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default="bkash")
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    
    is_anonymous = models.BooleanField(default=False)  # Hide donor name publicly
    donated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-donated_at']
    
    def __str__(self):
        name = self.display_name
        return f"{name} donated {self.amount} BDT to {self.crisis_post.title}"
    
    @property
    def display_name(self):
        """Return donor name or 'Anonymous' if hidden"""
        if self.is_anonymous:
            return "Anonymous"
        if self.donor:
            return self.donor.username
        return self.donor_name or "Anonymous"


class DonationGoods(models.Model):
    crisis_post = models.ForeignKey(CrisisPost, on_delete=models.CASCADE, related_name="goods_donations")
    donor = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="goods_donations")
    donor_name = models.CharField(max_length=100, blank=True, null=True)
    donor_email = models.EmailField(blank=True, null=True)
    donor_phone = models.CharField(max_length=20, blank=True, null=True)
    
    item_description = models.TextField(help_text="Describe items: e.g., '10 blankets, 5kg rice, 20 bottles water'")
    quantity = models.CharField(max_length=100, blank=True, null=True, help_text="Optional: Total items count")
    delivery_method = models.CharField(max_length=100, blank=True, null=True, help_text="How will you deliver? e.g., 'Self-delivery', 'Courier'")
    message = models.TextField(blank=True, null=True)
    
    is_anonymous = models.BooleanField(default=False)
    donated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-donated_at']
        verbose_name_plural = "Donation Goods"
    
    def __str__(self):
        name = self.display_name
        return f"{name} donated goods to {self.crisis_post.title}"
    
    @property
    def display_name(self):
        """Return donor name or 'Anonymous' if hidden"""
        if self.is_anonymous:
            return "Anonymous"
        if self.donor:
            return self.donor.username
        return self.donor_name or "Anonymous"