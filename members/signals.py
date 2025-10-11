
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Member


@receiver(post_save, sender=User)
def create_member_for_superuser(sender, instance, created, **kwargs):
    """
    When a superuser/staff is created, automatically create a basic Member profile
    This ensures admins appear in the member list
    """
    if created and (instance.is_superuser or instance.is_staff):
        # Check if member already exists for this user
        if not hasattr(instance, 'member_profile'):
            # Try to find existing member by username or email
            member = None
            if instance.username:
                member = Member.objects.filter(username=instance.username).first()
            if not member and instance.email:
                member = Member.objects.filter(email_address=instance.email).first()
            
            if member:
                # Link existing member to user
                member.user = instance
                member.is_staff = True
                member.save()
            else:
                # Create basic member profile - will need to be completed by admin
                # We'll create a minimal profile that can be updated later
                from datetime import date
                Member.objects.create(
                    user=instance,
                    first_name=instance.first_name or instance.username,
                    last_name=instance.last_name or 'Admin',
                    username=instance.username,
                    email_address=instance.email,
                    is_staff=True,
                    membership_status='Active',
                    # Set required fields with placeholders
                    gender='M',  # Default, should be updated
                    date_of_birth=date(1990, 1, 1),  # Placeholder, should be updated
                    marital_status='single',
                    location='To be updated',
                    education_level='other',
                    phone_number=f'UPDATE-{instance.username[:10]}',  # Temporary unique value
                    baptismal_first_name=instance.first_name or instance.username,
                    baptismal_last_name=instance.last_name or 'Admin',
                    date_baptized=date(2000, 1, 1),  # Placeholder
                    date_joined_religion=date(2000, 1, 1),  # Placeholder
                    # Note: Church structure fields will need to be set by admin
                    # These are required but we can't auto-fill them
                )


@receiver(post_save, sender=Member)
def create_user_for_member(sender, instance, created, **kwargs):
    """
    When a member is created/updated, create or update associated User account
    This allows members to login to the member portal
    """
    if not instance.user:
        # Only create user if member has email address
        if instance.email_address:
            # Check if user already exists with this username or email
            user = User.objects.filter(username=instance.username).first()
            if not user and instance.email_address:
                user = User.objects.filter(email=instance.email_address).first()
            
            if not user:
                # Create new user account
                user = User.objects.create_user(
                    username=instance.username,
                    email=instance.email_address,
                    first_name=instance.first_name,
                    last_name=instance.last_name,
                )
                # Set unusable password - member must use password reset to set password
                user.set_unusable_password()
                user.is_active = True  # Active so they can reset password
                user.is_staff = instance.is_staff  # Mirror staff status
                user.save()
                
                # Link user to member
                instance.user = user
                # Use update to avoid infinite loop
                Member.objects.filter(pk=instance.pk).update(user=user)
            elif not user.member_profile:
                # Link existing user to member
                instance.user = user
                Member.objects.filter(pk=instance.pk).update(user=user)
