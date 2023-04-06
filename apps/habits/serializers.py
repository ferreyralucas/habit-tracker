from rest_framework import serializers
from .models import Habit, HabitRecord


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'user', 'name', 'description', 'target', 'target_period', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class HabitRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitRecord
        fields = ['id', 'habit', 'date', 'completion', 'note', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
