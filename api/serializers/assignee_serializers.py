from rest_framework import serializers
from board import models
from .item_serializers import CommentAuthorSerializer


class AssigneeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Assignee
        fields = '__all__'


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
