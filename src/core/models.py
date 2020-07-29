from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """Custom user manager"""
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new custom user.
        Email, name, gender and password are obligatory fields.
        Other fields are passed as extras."""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """Create and save a new superuser, only email and password required.
        Called only from the command line."""
        superuser = self.create_user(email=email, password=password)
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.set_password(password)

        superuser.save(using=self._db)

        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user class with email as the identifier field"""
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    GENDERS = [
        (MALE, MALE),
        (FEMALE, FEMALE),
        (OTHER, OTHER),
    ]

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=6,
        choices=GENDERS,
        default=OTHER,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
