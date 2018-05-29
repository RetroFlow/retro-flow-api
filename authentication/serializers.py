from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', "username"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
