from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from core.router import router as core_router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(core_router.urls))
]

