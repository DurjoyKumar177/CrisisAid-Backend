from django.contrib import admin
from django.utils.html import format_html
from .models import CrisisPost, PostSection

@admin.register(CrisisPost)
class CrisisPostAdmin(admin.ModelAdmin):
    list_display = ("title", "post_type", "owner", "colored_status", "location", "created_at")
    list_filter = ("post_type", "status", "created_at")
    search_fields = ("title", "description", "owner__username", "location")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20
    
    # Color-coded status
    def colored_status(self, obj):
        colors = {
            'pending': 'orange',
            'approved': 'green',
            'rejected': 'red',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'
    
    # Quick actions for approval
    actions = ['approve_posts', 'reject_posts']
    
    def approve_posts(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} post(s) approved successfully.')
    approve_posts.short_description = 'Approve selected posts'
    
    def reject_posts(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} post(s) rejected.')
    reject_posts.short_description = 'Reject selected posts'


@admin.register(PostSection)
class PostSectionAdmin(admin.ModelAdmin):
    list_display = ("post", "section_type", "creator_name", "created_at")
    list_filter = ("section_type", "created_at")
    search_fields = ("post__title", "content", "created_by__username")
    readonly_fields = ("created_at",)