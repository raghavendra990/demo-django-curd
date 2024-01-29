

from rest_framework.serializers import (
    Serializer, ModelSerializer, SerializerMethodField, UUIDField,
    CharField, ChoiceField, EmailField, BooleanField, ListField, JSONField, )

class LoginSerializer(Serializer):  # pylint: disable=abstract-method
    """
    Login serializer
    """
    username = CharField(max_length=50 , required=True, allow_blank=False, allow_null=False)
    password = CharField(max_length=16,  required=True)

    