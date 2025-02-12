from treasures.models import Treasure
from users.models import CustomUser
from comments.models import Comment
from rest_framework import serializers
# I do not know why the above is complaining, I was able to import the module in the django shell

class TreasureSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    class Meta:
        model = Treasure
        fields = ["id","name","creator","category", "description","date_added","last_modified"]
        
class CommentSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    class Meta:
        model = Comment
        fields = ["id","creator","treasure","content","date_added","last_modified"]
        
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id","handle","email","date_joined","last_login"]