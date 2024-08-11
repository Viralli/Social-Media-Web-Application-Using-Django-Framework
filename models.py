from django.db import models
from django.conf import settings

class Profile(models.Model):
    """
    Profile model to extend the user model with additional information.
    Includes fields for user bio and profile picture.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name='User'
    )
    bio = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Bio'
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        blank=True, 
        null=True, 
        verbose_name='Profile Picture'
    )
    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class Post(models.Model):
    """
    Post model to represent a user post.
    Includes fields for title, content, author, and timestamps.
    """
    title = models.CharField(
        max_length=200, 
        verbose_name='Title'
    )
    content = models.TextField(
        verbose_name='Content'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name='Author'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='Updated At'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
