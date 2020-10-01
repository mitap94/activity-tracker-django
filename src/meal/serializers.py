from rest_framework import serializers

from core.models import BaseFood, FoodAmount, Recipe, Meal, DailyMeal


class BaseFoodSerializer(serializers.ModelSerializer):
    """Serializer for BaseFood objects"""

    class Meta:
        model = BaseFood
        fields = ('id', 'name', 'calories', 'serving_size', 'is_recipe', 'image')
        read_only_fields = ('id', 'is_recipe')


class FoodAmountSerializer(serializers.ModelSerializer):
    """Serializer for FoodAmount objects"""

    food = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=BaseFood.objects.all()
    )

    class Meta:
        model = FoodAmount
        fields = ('id', 'amount', 'food')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe objects"""
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=FoodAmount.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'calories', 'serving_size', 'is_recipe', 'image', 'instructions', 'ingredients')
        read_only_fields = ('id', 'is_recipe')


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for Recipe detail view"""
    ingredients = FoodAmountSerializer(many=True)


class MealSerializer(serializers.ModelSerializer):
    """Serializer for Meal objects"""
    meal_contents = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=FoodAmount.objects.all()
    )

    class Meta:
        model = Meal
        fields = ('id', 'calories', 'meal_contents')
        read_only_fields = ('id',)


class MealDetailSerializer(RecipeSerializer):
    """Serializer for Meal detail view"""
    meal_contents = FoodAmountSerializer(many=True)


class DailyMealSerializer(serializers.ModelSerializer):
    """Serializer for DailyMeal objects"""
    breakfast = serializers.PrimaryKeyRelatedField(
        many=False,
        allow_null=True,
        queryset=Meal.objects.all()
    )
    lunch = serializers.PrimaryKeyRelatedField(
        many=False,
        allow_null=True,
        queryset=Meal.objects.all()
    )
    diner = serializers.PrimaryKeyRelatedField(
        many=False,
        allow_null=True,
        queryset=Meal.objects.all()
    )
    snack = serializers.PrimaryKeyRelatedField(
        many=False,
        allow_null=True,
        queryset=Meal.objects.all()
    )

    class Meta:
        model = DailyMeal
        fields = ('id', 'date', 'calories', 'breakfast', 'lunch', 'diner', 'snack', 'water_glasses')
        read_only_fields = ('id',)


class DailyMealDetailSerializer(RecipeSerializer):
    """Serializer for DailyMeal detail view"""
    breakfast = MealSerializer(many=False)
    lunch = MealSerializer(many=False)
    diner = MealSerializer(many=False)
    snack = MealSerializer(many=False)
