from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# used to automate user registration process 
# helps decoupled applications get notified when actions occur elsewhere in the framework

# add receiver as a decorator in order to fire the function on specific event
@receiver(post_save, sender=User)
def build_profile(sender, instance, created, **kwargs):
    # instance - particular form/user
    # created - status of user creation process

    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()