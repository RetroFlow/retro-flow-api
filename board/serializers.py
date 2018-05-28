from rest_framework import serializers
from .models import (
    Board, BoardSettings, Column, Comment, Item, ItemStatus
)


class ItemStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemStatus
        fields = ['name']


class CommentSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    status = ItemStatusSerializer()

    class Meta:
        model = Item
        fields = '__all__'
