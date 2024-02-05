from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)


class CoreUserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError("An username is required.")
        if not password:
            raise ValueError("A password is required.")
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **kwargs):
        if not username:
            raise ValueError("An username is required.")
        if not password:
            raise ValueError("A password is required.")
        user = self.create_user(username, password)
        user.is_superuser = True
        user.first_name = kwargs["first_name"]
        user.last_name = kwargs["last_name"]
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user


class CoreUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True,null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = CoreUserManager()

    class Meta:
        db_table = "core_users"
