from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile, ClientProfile
from listdoctors.models import Doctor

@receiver(post_save, sender=CustomUser)
def create_user_profiles(sender, instance, created, **kwargs):
    if created:
        role = 'admin' if instance.is_superuser else 'patient'
        if not hasattr(instance, 'user_profile'):
            profile = UserProfile.objects.create(user=instance, role=role)
        if not hasattr(instance, 'client_profile'):
            ClientProfile.objects.create(user=instance)
        if role == 'doctor' and not hasattr(instance, 'user_profile'):
            Doctor.objects.create(user_profile=profile)
