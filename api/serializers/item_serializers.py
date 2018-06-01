from rest_framework.serializers import ModelSerializer
from board.models import ItemStatus, Item, Profile, Comment, Vote, Column
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

    author_info = CommentAuthorSerializer(read_only=True, source='author')

    class Meta:
        model = Comment
        fields = ['id', 'item_id', 'author_info', 'created_at', 'text']

    def create(self, validated_data):
        validated_data['item_id'] = self.context['view'].kwargs['item_pk']
        validated_data['author_id'] = self.context['view'].request.user.profile.id
        return ModelSerializer.create(self, validated_data)


class VoteSerializer(ModelSerializer):
    profile_info = CommentAuthorSerializer(read_only=True, source='profile')
    item_id = serializers.PrimaryKeyRelatedField(source='item', queryset=Item.objects.all())

    class Meta:
        model = Vote
        fields = ['profile_id', 'item_id', 'profile_info']

    def create(self, validated_data):
        validated_data['profile_id'] = self.context['view'].request.user.profile.id
        return ModelSerializer.create(self, validated_data)


class ItemSerializer(ModelSerializer):
    votes = VoteSerializer(read_only=True, many=True)
    status = serializers.SlugRelatedField(slug_field='code', required=False, queryset=ItemStatus.objects.all())
    column_id = serializers.PrimaryKeyRelatedField(queryset=Column.objects.all(), source='column')

    class Meta:
        model = Item
        fields = ['id', 'votes', 'vote_count', 'created_at',
                  'updated_at', 'author_id', 'heading',
                  'description', 'status', 'column_id']

    def create(self, validated_data):
        validated_data['author_id'] = self.context['view'].request.user.profile.id
        return ModelSerializer.create(self, validated_data)


class PlainItemSerializer(ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'heading']
