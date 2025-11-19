from django.contrib import admin
from django.utils.html import format_html
from .models import VolunteerApplication

@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    # Columns to show
    list_display = ("id", "user_name", "crisis_title", "colored_status", "applied_at")
    
    # Filters on sidebar
    list_filter = ("status", "crisis_post", "applied_at")
    
    # Search by username or post title
    search_fields = ("user__username", "crisis_post__title")
    
    # Ordering (latest first)
    ordering = ("-applied_at",)
    
    # Make applied_at read-only
    readonly_fields = ("applied_at",)
    
    # Optional: clickable link to user or crisis post
    list_display_links = ("user_name", "crisis_title")
    
    # Custom display methods
    def user_name(self, obj):
        return obj.user.username
    user_name.short_description = "Volunteer"

    def crisis_title(self, obj):
        return obj.crisis_post.title
    crisis_title.short_description = "Crisis Post"

    def colored_status(self, obj):
        color = {
            "pending": "orange",
            "approved": "green",
            "rejected": "red"
        }.get(obj.status, "black")
        return format_html(
            '<b><span style="color: {};">{}</span></b>',
            color,
            obj.status.capitalize()
        )
    colored_status.short_description = "Status"
    colored_status.admin_order_field = "status"
