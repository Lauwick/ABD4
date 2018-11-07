
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from vdm import views

router = DefaultRouter()
router.register(r'reservations', views.ReservationViewSet)
router.register(r'spectators', views.SpectatorViewSet)

app_name = 'vdm'

urlpatterns = [
    url(r'^api/(?P<version>(v1))/', include(router.urls)),
]
