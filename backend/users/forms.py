from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

# I think this is an irrelevant file now since I will be using react on the front end.

class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = (
            "email",
        )


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "email",
        )
