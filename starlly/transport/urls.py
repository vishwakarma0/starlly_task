from django.urls import include, path
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('vehicles', VehicleViewset)
router.register('permits', PermitTrackerViewset)

urlpatterns = [
    path('', include(router.urls)),
    ]