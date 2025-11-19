from django.contrib import admin
from django.utils.html import format_html
from .models import VolunteerApplication

@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "user_name", "crisis_title", "colored_status", "applied_at")
    list_filter = ("status", "crisis_post", "applied_at")
    search_fields = ("user__username", "crisis_post__title", "message")
    ordering = ("-applied_at",)
    readonly_fields = ("applied_at",)
    list_display_links = ("user_name", "crisis_title")
    
    # NEW: Bulk actions
    actions = ['approve_applications', 'reject_applications']
    
    def approve_applications(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} application(s) approved.')
    approve_applications.short_description = 'Approve selected applications'
    
    def reject_applications(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} application(s) rejected.')
    reject_applications.short_description = 'Reject selected applications'
    
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