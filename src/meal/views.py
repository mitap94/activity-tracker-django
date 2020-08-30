from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import BaseFood, FoodAmount, Recipe, Meal, DailyMeal
from . import serializers


class DefaultViewSet(viewsets.ModelViewSet):
    """Default ViewSet for food"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only or all"""
        all = bool(
            int(self.request.query_params.get('all', 0))
        )
        queryset = self.queryset
        if not all:
            queryset = queryset.filter(user=self.request.user)

        return queryset.order_by('-name').distinct()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class BaseFoodViewSet(DefaultViewSet):
    """Manage BaseFood in the database"""
    queryset = BaseFood.objects.all()
    serializer_class = serializers.BaseFoodSerializer


class FoodAmountViewSet(DefaultViewSet):
    """Manage FoodAmount in the database"""
    queryset = FoodAmount.objects.all()
    serializer_class = serializers.FoodAmountSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only or all"""
        all = bool(
            int(self.request.query_params.get('all', 0))
        )
        queryset = self.queryset
        if not all:
            queryset = queryset.filter(user=self.request.user)

        return queryset.order_by('-id')


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user only or all"""
        all = bool(
            int(self.request.query_params.get('all', 0))
        )
        queryset = self.queryset
        if not all:
            queryset = queryset.filter(user=self.request.user)
        
        return queryset.order_by('-id')

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        print(f'Dimitrije {serializer.data}')
        serializer.save(user=self.request.user)

class MealViewSet(viewsets.ModelViewSet):
    """Manage meals in the database"""
    serializer_class = serializers.MealSerializer
    queryset = Meal.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve meals for the authenticated user only"""
        queryset = self.queryset
        return queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.MealDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new meal"""
        meal_calories_sum = 0
        for food_amount in  serializer.validated_data['meal_contents']:
            meal_calories_sum = meal_calories_sum + food_amount.amount * food_amount.food.calories
        serializer.save(user=self.request.user, calories=meal_calories_sum)

class DailyMealViewSet(viewsets.ModelViewSet):
    """Manage daily meals in the database"""
    serializer_class = serializers.DailyMealSerializer
    queryset = DailyMeal.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve daily meals for the authenticated user only"""
        queryset = self.queryset
        return queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.DailyMealDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new daily meal"""
        daily_meal_calories_sum = 0
        breakfast = serializer.validated_data['breakfast']
        lunch = serializer.validated_data['lunch']
        diner = serializer.validated_data['diner']
        snack = serializer.validated_data['snack']
        if (breakfast):
            daily_meal_calories_sum = daily_meal_calories_sum + breakfast.calories
        if (lunch):
            daily_meal_calories_sum = daily_meal_calories_sum + lunch.calories
        if (diner):
            daily_meal_calories_sum = daily_meal_calories_sum + diner.calories
        if (snack):
            daily_meal_calories_sum = daily_meal_calories_sum + snack.calories
        serializer.save(user=self.request.user, calories=daily_meal_calories_sum)