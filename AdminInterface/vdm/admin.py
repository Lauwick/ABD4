from django.contrib import admin

from vdm.models import Game, Client, Spectator, Slot, Reservation, Tarif, Theme

# Register your models here.


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'game', 'slot', 'mail')
    list_filter = ('game',)
    ordering = ('slot',)
    search_fields = ('game',)
    fieldsets = (
        ('Reservation', {
            'fields': ('game', 'slot', 'mail')
        }),
        ('Joueurs', {
            'fields': ('spectators',)
        })
    )


class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme', 'vr')
    list_filter = ('name', 'theme', 'vr')
    # date_hierarchy = 'date'
    ordering = ('name',)
    search_fields = ('name',)
    fieldsets = (
        ('Jeu', {
            'fields': ('name', 'theme', 'vr',)
        }),
    )


class ClientAdmin(admin.ModelAdmin):
    list_display = ('civility', 'first_name', 'last_name', 'age')
    list_filter = ('civility',)
    # date_hierarchy = 'date'
    ordering = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    fieldsets = (
        ('Client', {
            'fields': ('civility', 'first_name', 'last_name', 'age')
        }),
    )


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Spectator)
admin.site.register(Slot)
admin.site.register(Tarif)
admin.site.register(Theme)
