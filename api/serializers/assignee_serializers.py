from rest_framework import serializers
from board import models
from .item_serializers import CommentAuthorSerializer


class GroupSerializer(serializers.ModelSerializer):
    members = CommentAuthorSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = models.Group
        fields = ['members', 'team_id', 'id', 'name', 'description']

    def create(self, validated_data):
        validated_data['team_id'] = self.context['view'].kwargs['team_pk']
        return serializers.ModelSerializer.create(self, validated_data)


class GroupMembersSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return validated_data

    members = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Profile.objects.all())


class AssigneeSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    profile = CommentAuthorSerializer(required=False, read_only=True)
    group = GroupSerializer(required=False, read_only=True)

    profile_id = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=models.Profile.objects.all())
    group_id = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=models.Group.objects.all())
    type = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = models.Assignee
        fields = ['profile_id', 'group_id', 'type', 'id', 'profile', 'group', 'item_id']

    def create(self, validated_data):

        item_id = self.context['view'].kwargs['item_pk']

        group = validated_data.get('group_id')
        profile = validated_data.get('profile_id')
        if group is not None:
            assignee = models.Assignee(item_id=item_id, group_id=group.id, type=models.Assignee.Type.GROUP)
        else:
            assignee = models.Assignee(item_id=item_id, profile_id=profile.id, type=models.Assignee.Type.USER)
        assignee.save()
        return assignee

    def validate(self, attrs):
        if attrs.get("profile_id") is None and attrs.get("group_id") is None:
            raise serializers.ValidationError('Exactly one of [Assignee.profile, Assignee.group] must be set')
        return serializers.ModelSerializer.validate(self, attrs)
