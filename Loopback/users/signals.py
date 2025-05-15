from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import Profile #User
from django.contrib.auth import get_user_model
from users.models import User

User = get_user_model()
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

#     else:
#         # Safely access the profile only if it exists
#         if hasattr(instance, 'profile'):
#             instance.profile.save()


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create profile for new user
        Profile.objects.create(user=instance)
    else:
        # Update existing profile if it exists
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            # Optionally, recreate profile if missing
            Profile.objects.create(user=instance)