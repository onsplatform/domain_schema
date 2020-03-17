from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from core.router import router as core_router
from core.views import CreateEntityView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(core_router.urls)),
    path('api/v1/import/data/', CreateEntityView.as_view()),
]

