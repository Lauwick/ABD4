from django.db import models
# Create your models here.


class Theme(models.Model):
    name = models.CharField('Thème', max_length=50, unique=True, null=False)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField('Name', max_length=50, unique=True, null=False)
    theme = models.ForeignKey(
        'vdm.Theme',
        verbose_name='Thème',
        related_name='jeux',
        null=False,
        on_delete=models.CASCADE
    )
    vr = models.BooleanField(verbose_name='Réalité Virtuelle', default=False)

    def __str__(self):
        return self.name


class Slot(models.Model):
    time = models.DateTimeField(null=False)

    @property
    def date(self):
        return self.time.strftime('%Y-%m-%d')

    def __str__(self):
        return self.time.strftime('%Y-%m-%d : %H-%M')


class Tarif(models.Model):
    name = models.CharField('Name', max_length=50, unique=True, null=False)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.name


class Client(models.Model):
    CIVILITIES = (
        (0, 'Monsieur'),
        (1, 'Madame'),
    )

    civility = models.PositiveSmallIntegerField(verbose_name='Civilité', choices=CIVILITIES)
    last_name = models.CharField('Nom', max_length=30, null=False)
    first_name = models.CharField('Prénom', max_length=30, null=False)
    age = models.PositiveIntegerField(verbose_name='Âge', null=False)

    @property
    def full_name(self):
        return ' '.join((self.first_name, self.last_name))

    def __str__(self):
        return self.full_name


class Spectator(models.Model):
    tarif = models.ForeignKey(
        'vdm.Tarif',
        verbose_name='Tarif',
        related_name='spectateurs',
        null=False,
        on_delete=models.CASCADE
    )
    client = models.ForeignKey(
        'vdm.Client',
        verbose_name='Client',
        related_name='spectateurs',
        null=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return ' '.join((self.client.__str__(), ' : ', self.tarif.__str__()))


class Reservation(models.Model):
    game = models.ForeignKey(
        'vdm.Game',
        verbose_name='Jeu',
        related_name='reservations',
        null=False,
        on_delete=models.CASCADE
    )
    slot = models.ForeignKey(
        'vdm.Slot',
        verbose_name='Créneau',
        related_name='reservations',
        null=False,
        on_delete=models.CASCADE
    )
    mail = models.EmailField(verbose_name='Email', null=False)
    spectators = models.ManyToManyField(
        'vdm.Spectator',
        related_name='reservations',
        null=False
    )

    def __str__(self):
        return ' '.join((self.game.__str__(), self.slot.__str__()))
