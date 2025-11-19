from django.contrib import admin
from django.utils.html import format_html
from .models import CrisisUpdate, Comment

@admin.register(CrisisUpdate)
class CrisisUpdateAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "crisis_post", "creator_display", "total_comments_display", "created_at")
    list_filter = ("crisis_post", "created_at", "created_by")
    search_fields = ("title", "description", "crisis_post__title", "created_by__username")
    readonly_fields = ("created_at", "updated_at", "total_comments")
    ordering = ("-created_at",)
    list_per_page = 20
    
    def creator_display(self, obj):
        return obj.created_by.username
    creator_display.short_description = "Created By"
    
    def total_comments_display(self, obj):
        count = obj.comments.count()
        if count > 0:
            return format_html('<b style="color: blue;">{} comment(s)</b>', count)
        return format_html('<i style="color: gray;">No comments</i>')
    total_comments_display.short_description = "Comments"
    
    fieldsets = (
        ('Update Information', {
            'fields': ('crisis_post', 'created_by', 'title', 'description', 'update_image')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'total_comments'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "commenter_display", "update_title", "text_preview", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("text", "user__username", "update__title")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    list_per_page = 30
    
    def commenter_display(self, obj):
        return obj.user.username
    commenter_display.short_description = "Commenter"
    
    def update_title(self, obj):
        return obj.update.title
    update_title.short_description = "Update"
    
    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = "Comment Text"