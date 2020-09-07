from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import UserGoal, Measurement
from . import serializers


class DefaultViewSet(viewsets.ModelViewSet):
    """Default ViewSet for measurements and goals"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        queryset = self.queryset
        return queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class UserGoalViewSet(DefaultViewSet):
    """Manage user goals in the database"""
    queryset = UserGoal.objects.all()
    serializer_class = serializers.UserGoalSerializer


class MeasurementViewSet(DefaultViewSet):
    """Manage user measurements in the database"""
    queryset = Measurement.objects.all()
    serializer_class = serializers.MeasurementSerializer
