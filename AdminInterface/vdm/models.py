from django.db import models
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.


class Theme(models.Model):
    name = models.CharField('Thème', max_length=50, unique=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Thème'


class ThemePriority(models.Model):
    game = models.ForeignKey(
        'vdm.Game',
        verbose_name='Jeu',
        related_name='jeu',
        null=False,
        on_delete=models.CASCADE
    )
    theme = models.ForeignKey(
        'vdm.Theme',
        verbose_name='Thème',
        related_name='themes',
        null=False,
        on_delete=models.CASCADE
    )
    priority = models.PositiveSmallIntegerField(verbose_name='Priorité', null=False)

    class Meta:
        ordering = ('priority',)
        verbose_name = 'Thème avec priorité'
        verbose_name_plural = 'Thèmes avec priorités'

    def __str__(self):
        return ' '.join((self.theme.name, ' : ', str(self.priority)))

    def save(self, *args, **kwargs):
        if not self.priority:
            try:
                nb = ThemePriority.objects.filter(game=self.game).count()
                self.priority = nb + 1
            except ObjectDoesNotExist:
                nb = 1
        super(ThemePriority, self).save()


class Game(models.Model):
    name = models.CharField('Name', max_length=50, unique=True, null=False)
    themes = models.ManyToManyField(
        'vdm.Theme',
        verbose_name='Thème',
        related_name='jeux',
        null=False,
        symmetrical=True,
        through='vdm.ThemePriority'
    )
    vr = models.BooleanField(verbose_name='Réalité Virtuelle', default=False)

    def __str__(self):
        return self.name

    def get_main_theme(self):
        return self.themes.first()
    get_main_theme.short_description = 'Thème principal'

    main_theme = property(get_main_theme)

    class Meta:
        verbose_name = 'Jeu'
        verbose_name_plural = 'Jeux'


class Slot(models.Model):
    time = models.DateTimeField(null=False)

    @property
    def date(self):
        return self.time.strftime('%Y-%m-%d')

    def __str__(self):
        return self.time.strftime('%Y-%m-%d : %H-%M')

    class Meta:
        ordering = ('time',)
        verbose_name = 'Créneau'
        verbose_name_plural = 'Créneaux'


class Tarif(models.Model):
    name = models.CharField('Nom', max_length=50, unique=True, null=False)
    amount = models.DecimalField(verbose_name='Prix', max_digits=9, decimal_places=2)

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

    class Meta:
        verbose_name = 'Spectateur'


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

    class Meta:
        verbose_name = 'Réservation'
        order_with_respect_to = 'slot'

    def __str__(self):
        return ' '.join((self.game.__str__(), self.slot.__str__()))
