from rest_framework.serializers import ModelSerializer
from board.models import ItemStatus, Item, Profile, Comment, Vote
from rest_framework import serializers


class ItemStatusSerializer(ModelSerializer):
    """ Serializer for item status"""
    class Meta:
        model = ItemStatus
        fields = '__all__'


class CommentAuthorSerializer(ModelSerializer):
    """Serializer for Profile models for usage with comments"""
    class Meta:
        model = Profile
        fields = ['username', 'full_name', 'icon', 'pk']


class CommentSerializer(ModelSerializer):

    author = CommentAuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class VoteSerializer(ModelSerializer):
    author = CommentAuthorSerializer(read_only=True, source='profile')
    profile_id = serializers.PrimaryKeyRelatedField(source='profile', queryset=Profile.objects.all())
    item_id = serializers.PrimaryKeyRelatedField(source='item', queryset=Item.objects.all())
    class Meta:
        model = Vote
        fields = ['profile_id', 'item_id', 'author']


class ItemSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, required=False, read_only=True)
    votes = VoteSerializer(read_only=True, many=True)

    class Meta:
        model = Item
        fields = '__all__'
