from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers

from api.serializers import MovieViewSet

router = routers.DefaultRouter()
router.register(r"movies", MovieViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
