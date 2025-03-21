from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib import messages

# Create your models here.

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    handle = models.CharField(
        _("handle"), max_length=30, unique=True, blank=True, null=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.handle:
            return self.handle
        return self.email.split("@")[0]

    def add_friend(self, friend):
        self.friends.add(friend)
        friend.friends.add(self)
        self.save()
        friend.save()

    @classmethod
    def dummy_user(cls):
        count = cls.dummy_count()
        email = f"dummy{count}@example.com"
        handle = f"dummy_{count}"
        user = User.objects.create_user(email=email, password="password", handle=handle)
        return user

    @classmethod
    def dummy_count(cls) -> int:
        return User.objects.filter(handle__startswith="dummy").count()

    def lookup_user(self, search_term, search_method):
        if search_term == "dummy test":
            friend = User.dummy_user()
            msg = f"{friend.handle} created."
            msg_type = messages.SUCCESS
        else:
            search_data = {search_method: search_term}
            try:
                friend = User.objects.get(**search_data)
            except User.DoesNotExist:
                friend = None
                msg = "User not found, please provide a valid handle or email."
                msg_type = messages.ERROR
            else:
                if friend.email == self.email:
                    msg = "You cannot add yourself as a friend."
                    msg_type = messages.ERROR
        return friend, msg, msg_type


class FriendshipRequest(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_requests"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_requests"
    )
    date_sent = models.DateTimeField(auto_now_add=True)
    date_responded = models.DateTimeField(null=True, blank=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.handle} to {self.receiver.handle}"

    def respond(self, accepted: bool):
        self.accepted = accepted
        self.date_responded = timezone.now()
        self.save()

    def accept(self, user):
        if user != self.receiver:
            return
        self.respond(True)
        self.receiver.add_friend(self.sender)
        self.sender.add_friend(self.receiver)

    def reject(self):
        self.respond(False)

    @classmethod
    def create_request(cls, sender, receiver):
        request = cls(sender=sender, receiver=receiver)
        request.save()
        # I don't think I need to return the request object currently.
        msg_type = messages.SUCCESS
        msg = f"Friend request sent to {receiver.handle}."
        return msg_type, msg
