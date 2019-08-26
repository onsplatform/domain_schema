from rest_framework import routers

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from core.views import SolutionView, AppView, EntityView, EntityMapView


__all__ = ['router', ]


schema_view = get_schema_view(title='ONS Platform Domain API', renderer_classes=[SwaggerUIRenderer, OpenAPIRenderer])


router = routers.SimpleRouter()
router.register('solution', SolutionView)
router.register('app', AppView)
router.register('entity', EntityView)
router.register('entitymap', EntityMapView),
router.register('entitymap/(?P<app_name>.+)/(?P<map_name>.+)', EntityMapView),
# router.register('swagger', schema_view)
