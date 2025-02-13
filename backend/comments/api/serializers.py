from ..models import Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = "__all__"
