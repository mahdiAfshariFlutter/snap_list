from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()  # برای اطمینان از اینکه پسوردی تنظیم نشده است
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        if username is None:
            email_username = email.split('@')[0]
            username = email_username
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email=email, username=username, password=password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username=username, password=password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True, error_messages={'unique': 'این ایمیل تکراری است'})
    avatar = models.URLField(blank=True, null=True)
    user_name = models.CharField(max_length=255)

    objects = UserManager()

    def __str__(self):
        return self.email


class OtpCode(models.Model):
    email = models.EmailField(blank=True, null=True)
    code = models.IntegerField(default=0)
