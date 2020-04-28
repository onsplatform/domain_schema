from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from core.router import router as core_router
from core.views import CreateEntityView, CreateMapMapView, AppVersionByReprocessableEntityView

api_version = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(api_version, include(core_router.urls)),
    path(api_version + 'create/entity/', CreateEntityView.as_view()),
    path(api_version + 'create/map/', CreateMapMapView.as_view()),
    path(api_version + 'appversion/byreprocessableentities', AppVersionByReprocessableEntityView.as_view())
]

