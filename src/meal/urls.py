from django.urls import path, include
from rest_framework.routers import DefaultRouter

from meal import views

app_name = 'meal'

router = DefaultRouter()
router.register('base_foods', views.BaseFoodViewSet)
router.register('recipes', views.RecipeViewSet)
router.register('food_amounts', views.FoodAmountViewSet)
router.register('meals', views.MealViewSet)
router.register('daily_meals', views.DailyMealViewSet)


# Authenticated users
# /api/meal/base_foods[/all] - list BaseFoods for current user [or for all users]
# /api/meal/base_foods/<id> - view detail of BaseFood
#
# /api/meal/food_amounts[/all] - list FoodAmounts for current user
# /api/meal/food_amounts/<id> - view detail of FoodAmount
#
# /api/meal/recipes[/all] - list Recipes for current user [or for all users]
# /api/meal/recipes/<id> - view detail of Recipe
#
# /api/meal/meals[/all] - list Meals for current user
# /api/meal/meals/<id> - view detail of Meal
#
# /api/meal/daily_meals[/all] - list DailyMeals for current user
# /api/meal/daily_meals/<id> - view detail of DailyMeal
#

urlpatterns = [
    path('', include(router.urls)),
]
