from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class PublicInfo(models.Model):
    email = models.EmailField(
        verbose_name=_('Additional email'),
        null=True,
        blank=True,
    )

    phone_number = models.CharField(
        max_length=15,
        verbose_name=_("Phone number"),
        null=True,
        blank=True,
    )

    additional_info = models.TextField(
        max_length=200,
        verbose_name=_('Additional info'),
        null=True,
        blank=True,
    )


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

    public_info = models.OneToOneField(
        PublicInfo,
        related_name='profile',
        verbose_name=_('Public info'),
        on_delete=models.CASCADE,
        null=True
    )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()


@receiver(post_save, sender=Profile)
def create_public_info_for_new_user(sender, created, instance, **kwargs):
    if created:
        public_info = PublicInfo.objects.create()
        instance.public_info = public_info
        public_info.save()  # TODO: check whether it is working approach

