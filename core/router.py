from rest_framework import routers

from core.views import SolutionView


__all__ = ['router', ]


router = routers.SimpleRouter()
router.register('solution', SolutionView)


