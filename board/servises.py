from .models import Board, BoardSettings, Team, UserRole


def get_default_board_setting():
    return BoardSettings.get_default_settings()


def create_new_team(user):
    team = Team()
    team.save()
    add_member_to_team(team=team, user=user, role=UserRole.Role.OWNER)
    return team


def add_member_to_team(user, team, **kwargs):
    team.add_member(user.profile, **kwargs)


def get_boards(user):
    return Board.objects.filter(team__members_info__profile_id=user.profile.id)


def get_teams(user):
    return Team.objects.filter(members_info__profile_id=user.profile.id)
