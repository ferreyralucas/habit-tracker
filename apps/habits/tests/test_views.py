from rest_framework.test import APITestCase
from .factories import UserFactory, HabitFactory, HabitRecordFactory
from ..models import Habit, HabitRecord


class HabitAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.habit = HabitFactory(user=self.user)
        self.habit_record = HabitRecordFactory(habit=self.habit)

    def test_create_habit(self):
        """
        This is a unit test in Python that checks if a habit can be created successfully.
        """
        url = '/habits/'
        data = {
            "name": "Test habit",
            "target": 5,
            "target_period": "daily"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 2)

    def test_list_habits(self):
        url = '/habits/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_update_habit(self):
        url = f'/habits/{self.habit.id}/'
        data = {
            "name": "Updated habit",
            "target": 7,
            "target_period": "weekly"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], data['name'])
        self.assertEqual(response.json()['target'], data['target'])
        self.assertEqual(response.json()['target_period'], data['target_period'])

    def test_delete_habit(self):
        url = f'/habits/{self.habit.id}/'
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Habit.objects.count(), 0)


class HabitRecordAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.habit = HabitFactory(user=self.user)
        self.habit_record = HabitRecordFactory(habit=self.habit)

    def test_create_habit_record(self):
        url = '/habit_records/'
        data = {
            "habit": self.habit.id,
            "date": "2023-04-01",
            "completion": 3
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(HabitRecord.objects.count(), 2)

    def test_list_habit_records(self):
        url = '/habit_records/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_update_habit_record(self):
        url = f'/habit_records/{self.habit_record.id}/'
        data = {
            "date": "2023-04-02",
            "completion": 4,
            "note": "Updated note"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['date'], data['date'])
