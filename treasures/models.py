from django.db import models
from users.models import CustomUser
# Create your models here.

class Treasure(models.Model):
    name = models.CharField(max_length=100)
    category = models.DecimalField(max_digits=10, decimal_places=2)
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
