from django.urls import path, include
from rest_framework.routers import DefaultRouter

from work import views


router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('works', views.WorkViewSet)

app_name = 'work'

urlpatterns = [
    path('', include(router.urls))
]
