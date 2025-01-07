from django.db import models
from users.models import CustomUser
from treasures.models import Treasure
# Create your models here.


def unknown_author():
    #should this be changed?
    return "Unknown Author"
class Comment(models.Model):
    content = models.TextField()
    treasure = models.ForeignKey('treasures.Treasure', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.SET(unknown_author))
    date_added = models.DateTimeField(auto_now_add=True)
    # I don't think I want to allow for comments to be edited.
    last_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.author.handle} said: {self.content}"
    
    def abbrev(self):
        return f"{self.author.handle} said: {self.content[:50]}"
