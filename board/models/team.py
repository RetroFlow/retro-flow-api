from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        on_delete=models.CASCADE,
        verbose_name=_('Related User instance'),
    )

    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('First name')
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('Last name')
    )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()

