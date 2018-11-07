
from rest_framework import serializers
from vdm.models import Game, Client, Spectator, Slot, Reservation, Tarif, Theme, ThemePriority


class SlotSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%Y-%m-%d : %H-%M')

    class Meta:
        model = Slot
        fields = ('time', )


class TarifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarif
        fields = ('name', 'amount')


class ClientSerializer(serializers.ModelSerializer):
    civility = serializers.CharField(source='get_civility_display')

    class Meta:
        model = Client
        fields = ('civility', 'last_name', 'first_name', 'age')


class SpectatorSerializer2(serializers.ModelSerializer):
    tarif = TarifSerializer()
    client = ClientSerializer()

    class Meta:
        model = Spectator
        fields = ('tarif', 'client',)


class SpectatorSerializer(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        return ' '.join((value.client.__str__(), value.tarif.__str__()))

    class Meta:
        model = Spectator
        fields = ('tarif', 'client',)


class ThemeSerializer(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        return value.name

    class Meta:
        model = Theme
        fields = ('name',)


class GameSerializer(serializers.ModelSerializer):
    themes = ThemeSerializer(many=True, queryset=Theme.objects.all())

    class Meta:
        model = Game
        fields = ('name', 'themes', 'vr')


class ReservationSerializer(serializers.ModelSerializer):
    game = GameSerializer()
    spectators = SpectatorSerializer2(many=True)
    # spectators = serializers.StringRelatedField(many=True)
    # spectators = SpectatorSerializer(many=True, queryset=Spectator.objects.all())
    slot = SlotSerializer()

    class Meta:
        model = Reservation
        fields = ('game', 'slot', 'mail', 'spectators')
