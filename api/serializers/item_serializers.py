from rest_framework.serializers import ModelSerializer
from board.models import ItemStatus, Item, Profile, Comment


class ItemStatusSerializer(ModelSerializer):
    """ Serializer for item status"""
    class Meta:
        model = ItemStatus
        fields = '__all__'


class CommentAuthorSerializer(ModelSerializer):
    """Serializer for Profile models for usage with comments"""
    class Meta:
        models = Profile
        fields = ['username', 'full_name', 'icon', 'pk']


class CommentSerializer(ModelSerializer):

    author = CommentAuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
