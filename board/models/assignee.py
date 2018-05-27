from django.db import models


class Assignee(models.Model):
    @property
    def assignee(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    @property
    def icon(self):
        raise NotImplementedError

    class Meta:
        abstract = True


class GroupAssignee(Assignee):
    def __init__(self, group, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = group
        self.Assignee = group.__class__

    @property
    def assignee(self):
        return self.group

    @property
    def name(self):
        return self.group.name

    @property
    def icon(self):
        return self.group.icon


class UserProfileAssignee(Assignee):
    def __init__(self, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = profile
        self.Assignee = profile.__class__

    @property
    def assignee(self):
        return self.profile

    @property
    def name(self):
        return self.profile.full_name

    @property
    def icon(self):
        return self.profile.icon
