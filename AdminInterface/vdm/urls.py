
from django.conf.urls import url, include
from vdm import views

app_name = 'vdm'

urlpatterns = [
    url(r'^api/(?P<version>(v1))/reservation', views.ReservationView)
]
