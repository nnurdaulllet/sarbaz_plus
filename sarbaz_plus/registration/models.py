from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
import random
import string
from django.utils import timezone
from datetime import timedelta


class PersonManager(BaseUserManager):
    def create_user(self, iin, password=None, **extra_fields):
        if not iin:
            raise ValueError('The IIN must be set')
        user = self.model(iin=iin, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, iin, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(iin, password, **extra_fields)

class Person(AbstractBaseUser, PermissionsMixin):
    iin = models.CharField(max_length=16, unique=True)

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    date_of_birthday = models.DateField(blank=True)
    address = models.CharField(max_length=255, blank=True, default='')
    phone_number = models.BigIntegerField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    USERNAME_FIELD = 'iin'
    REQUIRED_FIELDS = ["middle_name", "date_of_birthday", "email", 'first_name', 'last_name', 'address', 'phone_number']

    objects = PersonManager()

    def __str__(self):
        return f"{self.iin}"


class EmailVerification(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Проверяем, что код не истек (например, код действителен 10 минут)
        return timezone.now() <= self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"Verification for {self.email} - Code: {self.code}"