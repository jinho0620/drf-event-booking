from django.urls import path
from rest_framework.routers import DefaultRouter

from events import views

urlpatterns = [
]

router = DefaultRouter()
router.register('', views.EventViewSet)
urlpatterns += router.urls