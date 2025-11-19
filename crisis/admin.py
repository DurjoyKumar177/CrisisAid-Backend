from django.contrib import admin
from .models import CrisisPost, PostSection

@admin.register(CrisisPost)
class CrisisPostAdmin(admin.ModelAdmin):
    list_display = ("title", "post_type", "owner", "status", "created_at")
    list_filter = ("post_type", "status", "created_at")
    search_fields = ("title", "description", "owner__username")

@admin.register(PostSection)
class PostSectionAdmin(admin.ModelAdmin):
    list_display = ("post", "section_type")
