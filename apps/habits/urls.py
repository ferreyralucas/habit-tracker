from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, HabitRecordViewSet

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')
router.register(r'habit_records', HabitRecordViewSet, basename='habit_record')

urlpatterns = [
    path('', include(router.urls)),
]
