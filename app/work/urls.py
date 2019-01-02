from django.urls import path, include
from rest_framework.routers import DefaultRouter

from work import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.CategoryViewSet)

app_name = 'work'

urlpatterns = [
    path('', include(router.urls))
]
