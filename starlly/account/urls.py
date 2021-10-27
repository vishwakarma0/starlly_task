from django.urls import include, path
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('users', UserViewset)

urlpatterns = [
    path('samp/', samp, name="samp"),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    ]


