from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager  # AbstractBaseUser - user creation
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
import os


# BaseUserManager- managing users


# Create your models here.

def get_default_profile_image():
    return "default.png"


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Please input an email address")
        if not username:
            raise ValueError("Please input a username")

        user = self.model(
            email=self.normalize_email(email),  # normalize email can only be called in BaseUserManager
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'


def get_profile_image_filename(self):
    return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]


def get_profile_song_filepath(self, filename):
    return f"profile_songs/{self.pk}/{'profile_song.mp3'}"


def get_profile_song_filename(self):
    return str(self.profile_song)[str(self.profile_song).index(f'profile_songs/{self.pk}/'):]

def get_profile_background_filepath(self, filename):
    return f"profile_backgrounds/{self.pk}/{'profile_background.png'}"


def get_profile_background_filename(self):
    return str(self.profile_background)[str(self.profile_background).index(f'profile_backgrounds/{self.pk}/'):]

def has_module_perms(self, app_label):
    return self.is_superuser


class UserAccount(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=50, unique=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now='True')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    profile_image = models.ImageField(upload_to=get_profile_image_filepath, blank=True, null=True,
                                      default=get_default_profile_image)
    profile_song = models.FileField(upload_to=get_profile_song_filepath, blank=True, null=True)
    profile_background = models.ImageField(upload_to=get_profile_background_filepath, blank=True, null=True)
    hide_email = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    # shows what to be displayed when creating user object
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_superuser
    # return True
