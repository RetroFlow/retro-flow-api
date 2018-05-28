from django.db import models
from itertools import chain
from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _
from .team import Team, Group, GroupAssignee, Profile, UserProfileAssignee
from enum import Enum
from djchoices import ChoiceItem, DjangoChoices


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


class BoardSettings(models.Model):

    sprint_start_date = models.DateField()

    sprint_duration = models.DurationField()
    discussion_period = models.DurationField()

    icon = models.URLField(
        verbose_name=_('Link to board avatar image'),
        null=True,
        blank=True
    )

    @property
    def active_statuses(self):
        return ItemStatus.objects.filter(is_active=True)

    @classmethod
    def get_default_settings(cls):
        settings = BoardSettings(
            sprint_start_date=datetime.today(),
            sprint_duration=timedelta(weeks=2),
            discussion_period=timedelta(days=4)
        )

        return settings


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


class Column(models.Model):
    name = models.CharField(max_length=40)
    board = models.ForeignKey(
        'Board',
        related_name='columns',
        on_delete=models.CASCADE
    )


class Sprint(models.Model):
    start_date = models.DateField(
        verbose_name=_('Start date'),
        auto_now=True
    )

    duration = models.DurationField(
        verbose_name=_('Duration')
    )
    board = models.ForeignKey(
        'Board',
        on_delete=models.CASCADE,
        related_name='sprints'
    )

    def __str__(self):
        return "{}|{}".format(self.board.name, self.start_date)


class Board(models.Model):
    class Status(DjangoChoices):
        NEW = ChoiceItem('n', 'New')
        DISCUSSION = ChoiceItem('d', 'Discussion')
        RUNNING = ChoiceItem('r', 'Running')
        CLOSED = ChoiceItem('c', 'Closed')

    status = models.CharField(
        max_length=2,
        verbose_name=_('Board status - new, running or discussion period'),
        choices=Status.choices,
        default=Status.NEW
    )

    settings = models.OneToOneField(
        'BoardSettings',
        default=BoardSettings.get_default_settings,
        on_delete=models.SET_DEFAULT

    )

    current_sprint = models.ForeignKey(
        Sprint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='board_where_is_current'
    )

    previous_sprint = models.ForeignKey(
        Sprint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='board_where_is_previous'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: add board statuses
