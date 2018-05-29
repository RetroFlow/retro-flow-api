from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .assignee import GroupAssignee, UserProfileAssignee


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
        verbose_name=_('First name'),
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('Last name'),
    )

    icon = models.URLField(
        verbose_name=_('Link to user avatar image'),
        null=True,
        blank=True,
    )

    public_info = models.OneToOneField(
        PublicInfo,
        related_name='profile',
        verbose_name=_('Public info'),
        on_delete=models.CASCADE,
        null=True,
    )

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        return self.user.username

    @property
    def username(self):
        return self.user.username


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
        public_info.save()  # TODO: check whether it is a working approach


class UserRole(models.Model):
    class Role:
        REGULAR_USER = 'user'
        OWNER = 'owner'
        ADMIN = 'admin'

    code = models.CharField(
        max_length=20,
        unique=True,
        null=True
    )
    description = models.TextField(
        max_length=200,
        null=True,
        blank=True,
    )

    @classmethod
    def get_default_role(cls):
        # TODO: add default role proper management
        return cls.objects.get(code=cls.Role.REGULAR_USER).id

    def __str__(self):
        return "{}".format(self.code)


class Team(models.Model):
    members = models.ManyToManyField(
        Profile,
        through='MembershipInfo',
        related_name='teams'
    )

    def get_assignees(self):
        res = list(map(GroupAssignee, self.groups.all()))
        res.extend(map(UserProfileAssignee, self.members.all()))
        return res


class Group(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_('Group name')
    )

    description = models.TextField(
        max_length=200,
        verbose_name=_('Description'),
        blank=True,
        null=True
    )

    icon = models.URLField(
        verbose_name=_('Link to group avatar image'),
        null=True,
        blank=True
    )

    members = models.ManyToManyField(
        Profile,
        verbose_name=_('Group members'),
        related_name='groups'
    )

    team = models.ForeignKey(
        Team,
        related_name='groups',
        verbose_name=_('Team'),
        on_delete=models.CASCADE,
    )


class MembershipInfo(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.DO_NOTHING,
        related_name='member_info',
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='members_info',
    )

    role = models.ForeignKey(
        UserRole,
        on_delete=models.SET_DEFAULT,
        default=UserRole.get_default_role,
    )

    created_at = models.DateTimeField(auto_now_add=True)
