from django.db import models
from users.models import CustomUser
from treasures.models import Treasure
# Create your models here.


def unknown_author():
    # should this be changed?
    return "Unknown Author"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    treasure = models.ForeignKey("treasures.Treasure", on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.SET(unknown_author))
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.handle} said: {self.content}"

    @property
    def abbrev(self):
        return f"{self.author.handle} said: {self.shortened}"

    @property
    def shortened(self):
        shortened = self.content[:50]
        if len(self.content) > 50:
            shortened += "..."
        return shortened
