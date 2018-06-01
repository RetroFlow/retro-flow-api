from django.core.management.base import BaseCommand
from django.db import transaction

from ...models.team import Team
from ...models.board import Board


class Command(BaseCommand):
    args = ''
    help = 'Just run and create default statuses and roles'


    def handle(self, *args, **options):
        for i in Team.objects.all():
            if str(i) == "":
        #        i.board = 33

                i.delete()
                # Team.objects.remove(id=i.id)