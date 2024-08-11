from django.contrib import admin
from .models import Profile, Post  # Import both Profile and Post models

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for the Post model."""
    
    # Fields to display in the list view
    list_display = ('title', 'author', 'created_at', 'updated_at')
    
    # Fields to search in the admin search box
    search_fields = ('title', 'content')
    
    # Filters for the list view
    list_filter = ('created_at', 'author')
    
    # Order of posts in the list view
    ordering = ('-created_at',)
    
    # Allows navigation by date hierarchy
    date_hierarchy = 'created_at'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for the Profile model."""
    
    # Fields to display in the list view
    list_display = ('user', 'profile_picture_display')

    def profile_picture_display(self, obj):
        """Display the profile picture in the admin list view."""
        if obj.profile_picture:
            return f'<img src="{obj.profile_picture.url}" style="width: 100px; height: auto;" />'
        return 'No picture'
    
    # Allow HTML tags in the profile_picture_display field
    profile_picture_display.allow_tags = True
    profile_picture_display.short_description = 'Profile Picture'
