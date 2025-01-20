from django.db import models
from users.models import CustomUser
# Create your models here.

class Treasure(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100) # should this be a choice or a list?
    # lists don't work, so then it would be many to many, and then a separate category model or something.
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        msg = f"{self.creator.handle} feels that {self.name} is a National Treasure."
        msg += f" Their reasoning is that {self.description}."
        return msg
    
    def abbrev(self):
        return f"{self.name} - {self.creator.handle} for {self.category}"
