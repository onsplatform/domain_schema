from rest_framework import routers

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from core.views import CreateEntityView, SolutionView, AppView, AppVersionView, EntityView, EntityMapView, BranchView

__all__ = ['router', ]

schema_view = get_schema_view(title='ONS Platform Domain API', renderer_classes=[SwaggerUIRenderer, OpenAPIRenderer])

router = routers.SimpleRouter()
router.register('solution/byname/(?P<solution_name>.+)', SolutionView)
router.register('solution', SolutionView)
router.register('app', AppView)
router.register('app/(?P<solution_id>.+)/(?P<name>.+)', AppView)
router.register('appversion', AppVersionView)
router.register('branch', BranchView)
router.register('branch/(?P<solution_name>.+)/(?P<branch_name>.+)', BranchView)
router.register('entity', EntityView)
router.register('entitymap', EntityMapView)
router.register('entitymap/(?P<app_name>.+)/(?P<app_version>.+)/(?P<map_name>.+)', EntityMapView)
# router.register('swagger', schema_view)
