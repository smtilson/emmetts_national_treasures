from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Treasure

User = get_user_model()


class BaseSerializerMixin:
    # Checks if field names are valid
    def _check_unknown_fields(self, data):
        # Get the known fields from the serializer
        known_fields = set(self.fields.keys())
        # Get the incoming fields from the data
        incoming_fields = set(data.keys())
        # Find any unknown fields
        unknown_fields = incoming_fields - known_fields
        if unknown_fields:
            raise serializers.ValidationError(
                {
                    field: f"{field} is not a recognized field."
                    for field in unknown_fields
                }
            )


class TreasureSerializer(serializers.ModelSerializer, BaseSerializerMixin):
    # I guess these fields are not required so taht I can use the serializer for updating
    creator = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    # do I want this to be read only? Or maybe there would be a special view that could allow for this?
    name = serializers.CharField(required=False, max_length=100)
    category = serializers.CharField(required=False)
    description = serializers.CharField(
        style={"base_template": "textarea.html"}, required=False
    )
    date_added = serializers.DateTimeField(required=False, read_only=True)
    last_modified = serializers.DateTimeField(required=False, read_only=True)
    creator_handle = serializers.SerializerMethodField()
    short_details = serializers.SerializerMethodField()
    truncated_description = serializers.SerializerMethodField()

    class Meta:
        model = Treasure
        # include = ["creator_name", "short_details", "truncated_description"]
        fields = [
            "id",
            "creator",
            "creator_handle",
            "name",
            "category",
            "description",
            "date_added",
            "last_modified",
            "short_details",
            "truncated_description",
        ]

    def validate_name(self, value):
        # I think this is where the parser is interacting with things
        if not value.strip():
            raise serializers.ValidationError("Name cannot be blank.")
        return value

    def get_creator_handle(self, obj):
        # user = User.objects.get(pk=obj.creator)
        # return user.handle
        return obj.creator.handle

    def get_short_details(self, obj):
        return obj.short_details

    def get_truncated_description(self, obj):
        return obj.truncated

    def to_internal_value(self, data):
        self._check_unknown_fields(data)
        return super().to_internal_value(data)
