from django.urls import path
from rest_framework.routers import DefaultRouter

from tracker.apps import TrackerConfig
from tracker.views import (PleasantHabitViewSet, PublishedUsefulHabitListView, UsefulHabitCreateView,
                           UsefulHabitDeleteView, UsefulHabitDetailView, UsefulHabitListView, UsefulHabitUpdateView)

app_name = TrackerConfig.name

router = DefaultRouter()
router.register(r'pleasant-habits', PleasantHabitViewSet)
urlpatterns = [
    path("useful-habits/create/", UsefulHabitCreateView.as_view(), name="create_useful_habit"),
    path("useful-habits/published/", PublishedUsefulHabitListView.as_view(), name="published_useful_habits"),
    path("useful-habits/", UsefulHabitListView.as_view(), name="useful_habits"),
    path("useful-habits/<int:pk>/", UsefulHabitDetailView.as_view(), name="useful_habit"),
    path("useful-habits/<int:pk>/delete/", UsefulHabitDeleteView.as_view(), name="delete_useful_habit"),
    path("useful-habits/<int:pk>/update/", UsefulHabitUpdateView.as_view(), name="update_useful_habit"),

] + router.urls
