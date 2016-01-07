from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    """
    A serializer class for serializing the SlackUsers
    """
    id = serializers.IntegerField()
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    photo = serializers.CharField()
