
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.URLField(blank=True, null=True, help_text='Profile picture URL')
    phone_number = models.CharField(max_length=15, blank=True)
    position = models.CharField(max_length=100, default='Church Administrator')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.position}"

    @property
    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture
        return 'https://i.imgur.com/UkrjXEc.jpg'
