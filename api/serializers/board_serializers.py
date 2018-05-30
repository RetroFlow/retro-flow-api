from rest_framework.serializers import ModelSerializer
from board.models import BoardSettings
from board.models.board import ColumnTemplate, Board, Sprint
from rest_framework import serializers


class BoardTemplateSerializer(ModelSerializer):
    class Meta:
        model = ColumnTemplate
        fields = ['name']


class BoardSettingsSerializer(ModelSerializer):
    column_names = BoardTemplateSerializer(many=True)

    class Meta:
        fields = ['sprint_start_date', 'discussion_period', 'icon', 'sprint_duration', 'column_names']
        model = BoardSettings

    def create(self, validated_data):
        templates = validated_data.pop('column_names')
        settings = BoardSettings.objects.create(**validated_data)
        for data in templates:
            ColumnTemplate.objects.create(settings=settings, **data)
        return settings


class BoardSerializer(ModelSerializer):
    settings = BoardSettingsSerializer(read_only=False)
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        fields = ['name', 'settings', 'status', 'created_at', 'team_id', 'id']
        model = Board
        read_only_fields = ('created_at', 'status', 'id', 'team_id')

    def create(self, validated_data):
        settings = validated_data.pop('settings')

        settings = BoardSettingsSerializer().create(settings)
        board = Board.objects.create(settings=settings, **validated_data)
        return board


class SprintSerializer(ModelSerializer):
    class Meta:
        model = Sprint
        fields = '__all__'
