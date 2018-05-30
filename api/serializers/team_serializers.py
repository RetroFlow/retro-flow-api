from rest_framework.serializers import ModelSerializer
from board.models import team as team_models
from rest_framework import serializers


class PublicInfoSerializer(ModelSerializer):

    class Meta:
        model = team_models.PublicInfo
        fields = '__all__'


class UserProfileSerializer(ModelSerializer):
    public_info = PublicInfoSerializer(required=False, read_only=False)

    class Meta:
        model = team_models.Profile
        fields = ['public_info', 'full_name', 'username', 'icon', 'last_name', 'first_name', 'id']


class MembershipSerializer(ModelSerializer):
    profile = UserProfileSerializer(read_only=True, required=False)
    role = serializers.SlugRelatedField(slug_field='code', queryset=team_models.UserRole.objects.all())

    class Meta:
        model = team_models.MembershipInfo
        fields = ['profile_id', 'team_id', 'role', 'created_at', 'id', 'profile']
        write_only_fields = ('profile_id', 'team_id')


class TeamSerializer(ModelSerializer):
    members_info = MembershipSerializer(many=True, read_only=True)

    class Meta:
        model = team_models.Team
        fields = ['id', 'members_info']
