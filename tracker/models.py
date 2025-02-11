from django.db import models

from users.models import User


class PleasantHabit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь",
                             help_text="Выберите пользователя", related_name="pleasant_habits", null=True, blank=True)
    action = models.CharField(max_length=255, verbose_name="Действие", help_text="Введите действие привычки")

    class Meta:
        verbose_name = "Приятная привычка"
        verbose_name_plural = "Приятные привычки"

    def __str__(self):
        return self.action


class UsefulHabit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь",
                             help_text="Выберите пользователя", related_name="useful_habits", null=True, blank=True)
    place = models.CharField(max_length=150, verbose_name="Место выполнения", help_text="Введите место выполнения")
    time = models.TimeField(verbose_name="Время начала выполнения", help_text="Введите время начала выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие", help_text="Введите действие привыки")
    related_habit = models.ForeignKey(PleasantHabit, on_delete=models.SET_NULL, verbose_name="Связанная привычка",
                                      help_text="Выберите связанную привычку", null=True, blank=True)
    periodicity = models.IntegerField(verbose_name="Периодичность",
                                      help_text="Укажите периодичность выполнения в днях", default=1)
    award = models.CharField(max_length=255, verbose_name="Вознаграждение", help_text="Укажите вознаграждение",
                             null=True, blank=True)
    duration = models.IntegerField(verbose_name="Продолжительность", help_text="Укажите продолжительность в секундах")
    is_published = models.BooleanField(verbose_name="Признак публичности", help_text="Опубликовать привычку?",
                                       default=True)

    class Meta:
        verbose_name = "Полезная привычка"
        verbose_name_plural = "Полезные привычки"

    def __str__(self):
        return self.action