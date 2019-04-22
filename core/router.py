from rest_framework import routers

from core.views import SolutionView, AppView, EntityView, EntityMapView


__all__ = ['router', ]


router = routers.SimpleRouter()
router.register('solution', SolutionView)
router.register('app', AppView)
router.register('entity', EntityView)
router.register('entitymap', EntityMapView)


