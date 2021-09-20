from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from api.views import top_250

urlpatterns = [
    path("admin/", admin.site.urls),
    path("movies/", top_250),
]
