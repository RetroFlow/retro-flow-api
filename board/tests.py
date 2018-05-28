from django.test import TestCase

from django.contrib.auth import get_user_model
from .models import team


class TestProfileModel(TestCase):

    def test_profile_creation(self):
        User = get_user_model()

        user = User.objects.create(
            email="test-user@mail.com", password="password11")
        # Check that a Profile instance has been crated
        self.assertIsInstance(user.profile, team.Profile)

        # Call the save method of the user to activate the signal
        # again, and check that it doesn't try to create another
        # profile instance
        user.save()
        self.assertIsInstance(user.profile, team.Profile)

    def test_public_info_creation(self):
        User = get_user_model()

        user = User.objects.create(
            email="test-user@mail.com", password="password11")
        # Check that a Profile instance has been crated
        self.assertIsInstance(user.profile, team.Profile)
        self.assertIsInstance(user.profile.public_info, team.PublicInfo)


class TestTeamCreation(TestCase):

    def test_single_user_addition(self):
        User = get_user_model()

        user = User.objects.create(
            email="test-user@mail.com", password="password11")
        user.save()

        new_team = team.Team()
        new_team.save()

        # TODO: remove role creation
        role = team.UserRole(name="name")
        role.save()

        # TODO: add "add_member" method to Team class
        membership = team.MembershipInfo(profile=user.profile, team=new_team, role=role)
        membership.save()

        self.assertEqual(new_team.members.first(), user.profile)
        self.assertEqual(new_team.get_assignees()[0].assignee, user.profile)

    def test_single_group_addition(self):
        User = get_user_model()

        user = User.objects.create(
            email="test-user@mail.com", password="password11")
        user.save()

        new_team = team.Team()
        new_team.save()

        group = team.Group(name='group_name', team=new_team)
        group.save()
        group.members.add(user.profile)


        self.assertEqual(new_team.get_assignees()[0].assignee, group)
       # self.assertContains(new_team.get_assignees(), group)

    def test_group_and_user_addition(self):
        User = get_user_model()

        user = User.objects.create(
            email="test-user@mail.com", password="password11")
        user.save()

        new_team = team.Team()
        new_team.save()

        # TODO: remove role creation
        role = team.UserRole(name="name")
        role.save()

        # TODO: add "add_member" method to Team class
        membership = team.MembershipInfo(profile=user.profile, team=new_team, role=role)
        membership.save()

        group = team.Group(name='group_name', team=new_team)
        group.save()
        group.members.add(user.profile)

        self.assertEqual(len(new_team.get_assignees()), 2)

    def test_several_assignee_addition(self):
        User = get_user_model()

        user1 = User.objects.create(
            email="test-user@mail.com", password="password11")
        user1.save()

        user2 = User.objects.create(
            email="test-user2@mail.com", password="password11")
        user2.save()

        new_team = team.Team()
        new_team.save()

        # TODO: remove role creation
        role = team.UserRole(name="name")
        role.save()

        # TODO: add "add_member" method to Team class
        membership1 = team.MembershipInfo(profile=user1.profile, team=new_team, role=role)
        membership1.save()

        membership2 = team.MembershipInfo(profile=user2.profile, team=new_team, role=role)
        membership2.save()

        group = team.Group(name='group_name', team=new_team)
        group.save()
        group.members.add(user1.profile)

        self.assertEqual(len(new_team.get_assignees()), 3)
