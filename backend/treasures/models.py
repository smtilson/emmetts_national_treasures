from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Treasure(models.Model):
    name = models.CharField(max_length=100, blank=False)
    category = models.CharField(
        max_length=100, blank=True
    )  # should this be a choice or a list?
    # lists don't work, so then it would be many to many, and then a separate category model or something.
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["creator", "id"]

    def __str__(self):
        msg = f"{self.creator.handle} feels that {self.name} is a National Treasure."
        msg += f" Their reasoning is that {self.description}."
        return msg

    # Why did I add this property?
    @property
    def ignore_fields(self):
        return {"id", "creator", "date_added", "last_modified"}

    @property
    def short_details(self):
        # the word for should be replaced with a dash
        return f"{self.name} - {self.category} by {self.creator.handle}"

    @property
    def truncated(self):
        truncated = f"{self.name} - {self.creator.handle} for {self.description[:50]}"
        if len(self.description) > 50:
            truncated += "..."
        return truncated
