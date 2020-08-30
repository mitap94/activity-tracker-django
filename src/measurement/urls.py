from django.urls import path, include
from rest_framework.routers import DefaultRouter

from measurement import views

app_name = 'measurement'

router = DefaultRouter()
router.register('goals', views.UserGoalViewSet)
router.register('measurements', views.MeasurementViewSet)


# Authenticated users
# /api/measurement/goals[/all] - list UserGoal for current user
# /api/measurement/goals/<id> - view detail of UserGoal
#
# /api/measurement/measurements[/all] - list Measurement for current user
# /api/measurement/measurements/<id> - view detail of Measurement
#

urlpatterns = [
    path('', include(router.urls)),
]
