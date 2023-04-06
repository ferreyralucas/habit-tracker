from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Habit, HabitRecord
from .serializers import HabitSerializer, HabitRecordSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing, creating, updating, and deleting habits.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class HabitRecordViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing, creating, updating, and deleting habit records.
    """
    queryset = HabitRecord.objects.all()
    serializer_class = HabitRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(habit__user=self.request.user)
