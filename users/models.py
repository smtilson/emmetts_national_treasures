from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your models here.

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    handle = models.CharField(_('handle'), max_length=30, unique=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    friends = models.ManyToManyField('self', symmetrical=False, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return self.handle

    def add_friend(self, friend):
        self.friends.add(friend)
        friend.friends.add(self)
        self.save()
        friend.save()
    
    @classmethod
    def dummy_user(cls) -> 'CustomUser':
        count = cls.dummy_count()
        email = f"dummy{count}@example.com"
        handle = f"dummy_{count}"
        user = CustomUser.objects.create_user(email=email, password="password", handle=handle)
        return user
    
    @classmethod
    def dummy_count(cls) -> int:
        return CustomUser.objects.filter(handle__startswith="dummy").count()
    
    def lookup_user(self, search_term, search_method):
        if search_term == "dummy test":
            friend = CustomUser.dummy_user()
            msg = f"{friend.handle} created."
            msg_type = messages.SUCCESS
        else:
            search_data = {search_method: search_term}
            try:
                friend = CustomUser.objects.get(**search_data)
            except CustomUser.DoesNotExist:
                friend = None
                msg = "User not found, please provide a valid handle or email."
                msg_type = messages.ERROR
            else:
                if friend.email == self.email:
                    msg = "You cannot add yourself as a friend."
                    msg_type = messages.ERROR
        return friend, msg, msg_type