from django.forms import ModelForm
from .models import Treasure


class TreasureCreationForm(ModelForm):
    class Meta:
        model = Treasure
        fields = (
            "name", "category", "description"
        )