
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when a new User is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    """Create or save UserProfile when User is saved"""
    if created:
        # Create UserProfile for new users
        UserProfile.objects.create(user=instance)
    else:
        # Save existing UserProfile
        if hasattr(instance, 'userprofile'):
            instance.userprofile.save()
