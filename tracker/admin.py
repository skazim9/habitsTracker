from django.contrib import admin

from tracker.models import PleasantHabit, UsefulHabit


@admin.register(UsefulHabit)
class UsefulHabitAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "place", "time", "action", "related_habit")
    search_fields = ("action",)
    ordering = ("id",)


@admin.register(PleasantHabit)
class PleasantHabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "action",
    )
    search_fields = ("action",)
    ordering = ("id",)
