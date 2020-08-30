from datetime import date
import uuid
import os

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


def profile_picture_file_path(instance, filename):
    """Generate file path for new profile picture"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/profile_picture/', filename)

def food_picture_file_path(instance, filename):
    """Generate file path for food picture"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/food_picture/', filename)


def measurement_picture_file_path(instance, filename):
    """Generate file path for measurement picture"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/measurement_picture/', filename)

class UserManager(BaseUserManager):
    """Custom user manager"""
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new custom user"""
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
    profile_picture = models.ImageField(blank=True, null=True, upload_to=profile_picture_file_path)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        if self.name == "":
            return f'{self.email}'
        return f'{self.name} ({self.email})'


class Measurement(models.Model):
    """Class for user measurements"""
    date = models.DateField(default=date.today)
    weight = models.PositiveSmallIntegerField(default=0)
    height = models.PositiveSmallIntegerField(default=0)
    neck = models.PositiveSmallIntegerField(default=0)
    chest = models.PositiveSmallIntegerField(default=0)
    biceps = models.PositiveSmallIntegerField(default=0)
    forearm = models.PositiveSmallIntegerField(default=0)
    abdomen = models.PositiveSmallIntegerField(default=0)
    hips  = models.PositiveSmallIntegerField(default=0)
    thigh = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(blank=True, null=True, upload_to=measurement_picture_file_path)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class UserGoal(models.Model):
    """Class used to hold user goals
    currently only hosting current and goal weight"""
    current_weight  = models.PositiveSmallIntegerField(default=0)
    goal_weight = models.PositiveSmallIntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

class BaseFood(models.Model):
    """Base food class to be used for a simple food and recipes"""
    name = models.CharField(max_length=255)
    calories = models.PositiveSmallIntegerField(default=0)
    serving_size = models.PositiveSmallIntegerField(default=100)
    image = models.ImageField(blank=True, null=True, upload_to=food_picture_file_path)
    is_recipe = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Recipe(BaseFood):
    """Recipe class used for standard meal recipes"""
    instructions = models.TextField(blank=True)


class FoodAmount(models.Model):
    """Class used to quantify food"""
    food = models.ForeignKey(
        'BaseFood',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(default=1)
    belongs_to_recipe = models.ForeignKey(
        'Recipe',
        related_name='ingredients',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    belongs_to_meal = models.ForeignKey(
        'Meal',
        related_name = 'meal_contents',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.amount} x {self.food.name}'


class Meal(models.Model):
    """Class for breakfast, lunch, diner and snacks"""
    calories = models.PositiveSmallIntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class DailyMeal(models.Model):
    """Class containing all of users meals for one day"""
    date = models.DateField(default=date.today)
    calories = models.PositiveSmallIntegerField(default=0)
    breakfast = models.ForeignKey(
        'Meal',
        blank=True,
        null=True,
        related_name='breakfast',
        on_delete=models.CASCADE,
    )
    lunch = models.ForeignKey(
        'Meal',
        blank=True,
        null=True,
        related_name='lunch',
        on_delete=models.CASCADE,
    )
    diner = models.ForeignKey(
        'Meal',
        blank=True,
        null=True,
        related_name='diner',
        on_delete=models.CASCADE,
    )
    snack = models.ForeignKey(
        'Meal',
        blank=True,
        null=True,
        related_name='snack',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    water_glasses = models.PositiveSmallIntegerField(default=0)