from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager

class UserManager(DjangoUserManager):
    def create_manager(self, name, email, country, password=None):
        user = self.model(
            username=email,
            email=email,
            first_name=name,
            country=country,
            is_staff=False,
            is_superuser=False,
            is_active=True,
            role='manager'
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')
        if extra_fields.get('role') != 'admin':
            raise ValueError('Superuser must have role=admin.')
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
    )
    country = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='manager')

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} ({self.email})"
