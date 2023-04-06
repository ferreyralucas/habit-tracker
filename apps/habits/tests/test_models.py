import pytest
from .factories import UserFactory, HabitFactory, HabitRecordFactory


@pytest.fixture
def test_user():
    return UserFactory()


@pytest.fixture
def test_habit(test_user):
    return HabitFactory(user=test_user)


@pytest.fixture
def test_habit_record(test_habit):
    return HabitRecordFactory(habit=test_habit)


def test_habit_creation(test_habit):
    assert test_habit.name
    assert test_habit.target
    assert test_habit.target_period


def test_habit_record_creation(test_habit_record):
    assert test_habit_record.habit.name
    assert test_habit_record.date
    assert test_habit_record.completion
