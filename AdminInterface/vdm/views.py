
from rest_framework import viewsets
from vdm.serializers import ReservationSerializer, SpectatorSerializer2
from vdm.models import Reservation, Spectator


class ReservationViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class SpectatorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Spectator.objects.all()
    serializer_class = SpectatorSerializer2
