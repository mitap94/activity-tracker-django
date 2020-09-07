from rest_framework import serializers

from core.models import UserGoal, Measurement


class UserGoalSerializer(serializers.ModelSerializer):
    """Serializer for UserGoal objects"""

    class Meta:
        model = UserGoal
        fields = ('id', 'current_weight', 'goal_weight')
        read_only_fields = ('id',)


class MeasurementSerializer(serializers.ModelSerializer):
    """Serializer for Measurement objects"""

    class Meta:
        model = Measurement
        fields = ('id', 'date', 'weight', 'height', 'neck', 'chest', 'biceps',
                  'forearm', 'abdomen', 'hips', 'thigh', 'image')
        read_only_fields = ('id',)
