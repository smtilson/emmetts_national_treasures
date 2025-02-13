from ..models import Treasure
from rest_framework import serializers
# I do not know why the above is complaining, I was able to import the module in the django shell


class TreasureSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()

    class Meta:
        model = Treasure
        fields = "__all__"
