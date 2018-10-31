from rest_framework import serializers
from vdm.models import Reservation


class ReservationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Reservation
        fields = ('game', 'slot', 'mail', 'spectators')
