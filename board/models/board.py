from django.db import models, transaction
from datetime import datetime, timedelta, date
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from djchoices import ChoiceItem, DjangoChoices
from django.db.models.signals import post_save
from .items import ItemStatus
from .team import Team


class BoardSettings(models.Model):

    sprint_start_date = models.DateTimeField()

    sprint_duration = models.IntegerField()
    discussion_period = models.IntegerField()

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

        settings = dict(
            sprint_start_date=datetime.today(),
            sprint_duration=14,
            discussion_period=4,
            column_names=[{'name': 'Start'}, {'name': 'Continue'}, {'name': 'Stop'}]
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
        related_name='column_names'
    )


class Sprint(models.Model):
    start_date = models.DateField(
        verbose_name=_('Start date'),
        auto_now=True
    )

    duration = models.IntegerField(
        verbose_name=_('Duration in days')
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

    name = models.CharField(
        max_length=40
    )

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
    team = models.OneToOneField(
        'Team',
        null=True,
        blank=True,
        related_name='board',
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def board(self):
        return self

    def move_to_discussion(self):
        self.status = self.Status.DISCUSSION
        self.save()

    def start_new_sprint(self):
        with transaction.atomic():
            new_sprint = Sprint(duration=self.settings.sprint_duration, board=self)
            new_sprint.save()

            for temp in self.settings.column_names.all():
                c = Column(sprint=new_sprint, name=temp.name)
                c.save()
            self.previous_sprint = self.current_sprint
            self.current_sprint = new_sprint
            self.status = self.Status.RUNNING
            self.save()

