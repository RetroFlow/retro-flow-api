from django.core.management.base import BaseCommand
from django.db import transaction

from ...models.team import UserRole
from ...models.board import ItemStatus


class Command(BaseCommand):
    args = ''
    help = 'Just run and create default statuses and roles'

    def create_user_roles(self):
        user = UserRole(code=UserRole.Role.REGULAR_USER)
        user.save()

        owner = UserRole(code=UserRole.Role.OWNER)
        owner.save()

        admin = UserRole(code=UserRole.Role.ADMIN)
        admin.save()

    def create_item_statuses(self):
        new = ItemStatus(code=ItemStatus.Status.NEW, is_active=True)
        new.save()

        archived = ItemStatus(code=ItemStatus.Status.ARCHIVED, is_active=False)
        archived.save()

        closed = ItemStatus(code=ItemStatus.Status.CLOSED, is_active=False)
        closed.save()

        in_process = ItemStatus(code=ItemStatus.Status.IN_PROGRESS, is_active=True)
        in_process.save()

        pending = ItemStatus(code=ItemStatus.Status.PENDING, is_active=True)
        pending.save()

        done = ItemStatus(code=ItemStatus.Status.DONE, is_active=False)
        done.save()

    def handle(self, *args, **options):
        self.create_user_roles()
        self.create_item_statuses()
