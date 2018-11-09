# Generated by Django 2.1.2 on 2018-11-08 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vdm', '0004_auto_20181107_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='spectators',
            field=models.ManyToManyField(blank=True, related_name='reservations', to='vdm.Spectator'),
        ),
        migrations.AlterField(
            model_name='tarif',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='themepriority',
            name='priority',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='Priorité'),
        ),
        migrations.AlterField(
            model_name='themepriority',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='theme', to='vdm.Theme', verbose_name='Thème'),
        ),
    ]
