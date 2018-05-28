from django.db import models
from djchoices import ChoiceItem, DjangoChoices
from django.utils.translation import ugettext_lazy as _
from .team import Group, GroupAssignee, Profile, UserProfileAssignee


class ItemStatus(models.Model):
    code = models.CharField(
        max_length=64,
        unique=True,
    )

    description = models.TextField(
        max_length=200,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True
    )

    class Status:
        NEW = 'new'
        DONE = 'done'
        CLOSED = 'closed'
        IN_PROGRESS = 'in_progress'
        ARCHIVED = 'archived'
        PENDING = 'pending'

    @classmethod
    def get_default_item_status(cls):
        return ItemStatus.objects.get(code=cls.Status.NEW)

    def __str__(self):
        return "{}".format(self.code)

# TODO: deal with custom item statuses
# class CustomItemStatus(AbstractItemStatus):
#     board_setting = models.ForeignKey(
#         'BoardSettings',
#         related_name='custom_statuses',
#         on_delete=models.CASCADE
#     )
#
#     @property
#     def board(self):
#         return self.board_setting.board


class Comment(models.Model):
    item = models.ForeignKey('Item', related_name='comments', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Comment body')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Assignee(models.Model):
    class Type(DjangoChoices):
        USER = ChoiceItem('u', 'User')
        GROUP = ChoiceItem('g', 'Group')

    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
        related_name='assignees',

    )

    type = models.CharField(
        max_length=2,
        verbose_name=_('Assignee type - User or Group'),
        choices=Type.choices,
        default=Type.USER
    )

    group = models.ForeignKey(
        Group,
        related_name='assignments',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    profile = models.ForeignKey(
        Profile,
        related_name='assignments',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    @property
    def assignee(self):
        if self.type == self.Type.USER:
            return UserProfileAssignee(self.profile)
        else:
            return GroupAssignee(self.group)

    def save(self, *args, **kwargs):
        if self.group and self.profile or not self.group and not self.profile:
            raise ValueError('Exactly one of [Assignee.profile, Assignee.group] must be set')

        super().save(self, *args, **kwargs)


class Item(models.Model):
    column = models.ForeignKey(
        'Column',
        related_name='items',
        on_delete=models.CASCADE
    )

    heading = models.CharField(max_length=125)

    description = models.TextField(blank=True, null=True)

    status = models.ForeignKey(
        ItemStatus,
        default=ItemStatus.get_default_item_status,
        on_delete=models.SET_DEFAULT,
    )

    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='items',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_assignees(self):
        return map(lambda assign: assign.assignee, self.assignees)


class Vote(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='votes',
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='items',
    )
