
from rest_framework.serializers import (Serializer, ModelSerializer, PrimaryKeyRelatedField,
                                        SerializerMethodField, UUIDField, IntegerField, CharField, ReadOnlyField,
                                        ChoiceField, FloatField, DateField, ListField, )
from .models import Item

from userauth.serializers import LoginSerializer
class ItemListSerializer(ModelSerializer):
    """
    ItemListSerializer
    """
    user = LoginSerializer(required=False, read_only=True)

    class Meta:
        """
        Item Serializer Meta class
        """
        model = Item
        fields = (
            'id', 'name', 'user', 'price', 'created_at', 'updated_at', 'created_by',
            'updated_by',
        )

        read_only_fields = (
            'id',
            'created_at',
            'created_by',
        )
    

class ItemGetCreateUpdateSerializer(ModelSerializer):
    """
    ItemListSerializer
    """
    user = LoginSerializer(required=False, read_only=True)

    class Meta:
        """
        Item Serializer Meta class
        """
        model = Item
        fields = (
            'id', 'name', 'user', 'price', 'created_at', 'updated_at', 'created_by',
            'updated_by',
        )

        read_only_fields = (
            'id',
            'user'
            'created_at',
            'created_by',
        )
    
