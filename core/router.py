from rest_framework import routers

from core.views import SolutionView, AppView


__all__ = ['router', ]


router = routers.SimpleRouter()
router.register('solution', SolutionView)
router.register('app', AppView)


