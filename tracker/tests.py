from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tracker.models import PleasantHabit, UsefulHabit
from users.models import User


class UsefulHabitTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email="test@test.ru", chat_id="123")
        self.client.force_authenticate(user=self.user)
        self.pleasant_habit = PleasantHabit.objects.create(action="Well done")
        self.useful_habit = UsefulHabit.objects.create(
            place="home", time="13:00", action="Run", related_habit=self.pleasant_habit, duration=12, user=self.user
        )

    def test_useful_habit_create(self):
        url = reverse("tracker:create_useful_habit")
        data = {
            "place": "home",
            "time": "12",
            "action": "Run",
            "duration": 120,
            "related_habit": self.pleasant_habit.pk,
            "user": self.user.pk,
        }
        response = self.client.post(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result.get("time"), "12:00:00")
        self.assertEqual(result.get("periodicity"), 1)
        self.assertEqual(UsefulHabit.objects.all().count(), 2)

    def test_useful_habit_detail(self):
        url = reverse("tracker:useful_habit", args=(self.useful_habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(self.useful_habit.user, self.user)
        self.assertEqual(data.get("periodicity"), self.useful_habit.periodicity)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("place"), self.useful_habit.place)

    def test_useful_habit_create_invalid_duration(self):
        url = reverse("tracker:create_useful_habit")
        data = data = {
            "place": "home",
            "time": "12",
            "action": "Run",
            "duration": 121,
            "related_habit": self.pleasant_habit.pk,
            "user": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("duration"), ["Максимальное время выполнения привычки 120 секунд"])
        self.assertEqual(UsefulHabit.objects.all().count(), 1)

    def test_useful_habit_create_invalid_award(self):
        url = reverse("tracker:create_useful_habit")
        data = data = {
            "place": "home",
            "time": "12",
            "action": "Run",
            "duration": 50,
            "related_habit": self.pleasant_habit.pk,
            "award": "cookies",
            "user": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("non_field_errors"), ["Выберите только один вариант поощрения"])
        self.assertEqual(UsefulHabit.objects.all().count(), 1)

    def test_useful_habit_create_invalid_periodicity(self):
        url = reverse("tracker:create_useful_habit")
        data = {
            "place": "home",
            "time": "12",
            "action": "Run",
            "duration": 120,
            "related_habit": self.pleasant_habit.pk,
            "user": self.user.pk,
            "periodicity": 8,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("periodicity"), ["Нельзя выполнять привычку реже, чем 1 раз в 7 дней"])
        self.assertEqual(UsefulHabit.objects.all().count(), 1)

    def test_useful_habit_list(self):
        url = reverse("tracker:useful_habits")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.useful_habit.pk,
                    "periodicity": 1,
                    "duration": self.useful_habit.duration,
                    "place": self.useful_habit.place,
                    "time": "13:00:00",
                    "action": self.useful_habit.action,
                    "award": None,
                    "is_published": True,
                    "user": self.user.pk,
                    "related_habit": self.useful_habit.related_habit.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_useful_habit_delete(self):
        url = reverse("tracker:delete_useful_habit", args=(self.useful_habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UsefulHabit.objects.all().count(), 0)

    def test_useful_habit_update(self):
        url = reverse("tracker:update_useful_habit", args=(self.useful_habit.pk,))
        data = {"action": "Jump"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "Jump")
