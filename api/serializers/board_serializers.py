from rest_framework.serializers import ModelSerializer
from board.models import BoardSettings


class BoardSettingsSerializer(ModelSerializer):
    class Meta:
        fields = ['sprint_start_date', 'discussion_period', 'icon', 'sprint_duration']
        model = BoardSettings
