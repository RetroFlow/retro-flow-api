from django.db import models
from datetime import datetime, timedelta, date
from django.utils.translation import ugettext_lazy as _
from djchoices import ChoiceItem, DjangoChoices
from .items import ItemStatus


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
            sprint_start_date=date.today(),
            sprint_duration=timedelta(weeks=2),
            discussion_period=timedelta(days=4)
        )

        return settings


class Column(models.Model):
    name = models.CharField(max_length=40)
    sprint = models.ForeignKey(
        'Sprint',
        related_name='columns',
        on_delete=models.CASCADE
    )

    @property
    def board(self):
        return self.sprint.board


class ColumnTemplate(models.Model):
    name = models.CharField(
        max_length=40,
        verbose_name=_('Name'),
    )
    settings = models.ForeignKey(
        'BoardSettings',
        on_delete=models.CASCADE,
        related_name='column_templates'
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
        #default=BoardSettings.get_default_settings,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,

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
