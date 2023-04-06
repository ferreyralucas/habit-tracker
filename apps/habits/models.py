from django.db import models
from django.contrib.auth.models import User
from enum import Enum
from utils.models import TimeStampedModel


class TargetPeriodChoices(Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Habit(TimeStampedModel):
    '''
    Habit model represents a specific habit a user wants to track
    '''
    # ForeignKey to relate Habit to a specific User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Name of the habit
    name = models.CharField(max_length=255)
    # Optional description of the habit
    description = models.TextField(blank=True, null=True)
    # Target number of repetitions for the habit
    target = models.IntegerField()
    # Choices for daily, weekly, or monthly targets
    target_period = models.CharField(
        max_length=255,
        choices=TargetPeriodChoices.choices()
    )

    def __str__(self):
        return self.name


class HabitRecord(TimeStampedModel):
    '''
    HabitRecord model represents a tracking record for a habit on a specific date
    '''
    # ForeignKey to relate HabitRecord to a specific Habit
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    # Date of the record
    date = models.DateField()
    # Number of times the habit was completed on this date
    completion = models.IntegerField()
    # Optional field for additional notes
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.habit.name} - {self.date}"
