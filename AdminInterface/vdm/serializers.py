
import pprint
from datetime import datetime
from rest_framework import serializers
from vdm.models import (
    Game as vdmGame,
    Client,
    Spectator,
    Slot,
    Reservation as vdmReservation,
    Tarif as vdmTarif,
    Theme,
    ThemePriority
)


CIVILITIES = {
    'Monsieur': 0,
    'Madame': 1,
}


class BuyerSerializer(serializers.Serializer):
    Civilite = serializers.CharField()
    Nom = serializers.CharField()
    Prenom = serializers.CharField()
    Age = serializers.IntegerField()
    Email = serializers.EmailField()


class StringListField(serializers.ListField):
    child = serializers.CharField()


class GameSerializer(serializers.Serializer):
    Nom = serializers.CharField()
    Jour = serializers.CharField()
    Horaire = serializers.CharField()
    VR = serializers.CharField()
    Themes = StringListField()


class SpectatorSerializer(serializers.Serializer):
    Civilite = serializers.CharField()
    Nom = serializers.CharField()
    Prenom = serializers.CharField()
    Age = serializers.IntegerField()


class PurchaseSerializer(serializers.Serializer):
    Spectateur = SpectatorSerializer()
    Tarif = serializers.CharField()


class ReservationSerializer(serializers.BaseSerializer):
    Acheteur = BuyerSerializer()
    Game = GameSerializer()
    Reservation = serializers.ListField(child=PurchaseSerializer())

    def to_internal_value(self, data):
        obj = data
        if not obj['Acheteur']:
            raise serializers.ValidationError({
                'Acheteur': 'This field is required.'
            })
        if not obj['Reservation']:
            raise serializers.ValidationError({
                'Reservation': 'This field is required.'
            })
        if not obj['Game']:
            raise serializers.ValidationError({
                'Game': 'This field is required.'
            })
        return {'data': data}

    def create(self, validated_data):
        """
        Create and return a new `Reservation` instance, given the validated data.
        """
        reservation = self._reservation_from_validated_data(validated_data)
        return reservation

    def _reservation_from_validated_data(self, validated_data):
        validated_data = validated_data['data']
        game = self._game_from_validated_data(validated_data['Game'])
        slot = self._slot_from_validated_data(validated_data['Game'])
        mail = validated_data['Acheteur']
        spectators = self._spectators_from_validated_data(validated_data['Reservation'])
        reservation = vdmReservation.objects.get_or_create(game=game, slot=slot, mail=mail)[0]
        for spectator in spectators:
            reservation.spectators.add(spectator)
        return reservation

    def _game_from_validated_data(self, validated_data):
        name = validated_data['Nom']
        themes = self._themes_from_validated_data(validated_data['Themes'])
        vr = True if "Oui" == validated_data['VR'] else False

        game = vdmGame.objects.get_or_create(name=name, vr=vr)[0]
        game.save()
        for theme in themes:
            ThemePriority.objects.get_or_create(game=game, theme=theme)
        game.save()
        return game

    def _spectators_from_validated_data(self, validated_data):
        spectators = []
        for obj in validated_data:
            client = self._client_from_validated_data(obj['Spectateur'])
            tarif = vdmTarif.objects.filter(name=obj['Tarif']).latest(field_name='pk')
            spectator = Spectator.objects.get_or_create(
                tarif=tarif,
                client=client
            )[0]
            spectators.append(spectator)

        return spectators

    def _themes_from_validated_data(self, validated_data):
        themes = []
        for obj in validated_data:
            theme = Theme.objects.get_or_create(name=obj)[0]
            themes.append(theme)
        return themes

    def _slot_from_validated_data(self, validated_data):
        time = datetime.strptime(' '.join((validated_data['Jour'], validated_data['Horaire'])), '%Y-%m-%d %H:%M')
        return Slot.objects.get_or_create(time=time)[0]

    def _client_from_validated_data(self, validated_data):
        civility = CIVILITIES[validated_data['Civilite']]
        last_name = validated_data['Nom']
        first_name = validated_data['Prenom']
        age = validated_data['Age']
        client = Client.objects.get_or_create(
            civility=civility,
            last_name=last_name,
            first_name=first_name,
            age=age
        )
        return client[0]









