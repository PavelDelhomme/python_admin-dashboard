from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import CustomUser, UserProfile

def create_default_groups(sender, **kwargs):
    Group.objects.get_or_create(name='Administrateur')
    Group.objects.get_or_create(name='Utilisateur')

post_save.connect(create_default_groups, sender=CustomUser)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()