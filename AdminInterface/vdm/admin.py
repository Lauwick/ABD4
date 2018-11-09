from django.contrib import admin

from vdm.models import Game, Client, Spectator, Slot, Reservation, Tarif, Theme, ThemePriority

# Register your models here.


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'game', 'slot', 'mail')
    list_filter = ('game',)
    ordering = ('-slot',)
    search_fields = ('game',)
    fieldsets = (
        ('Reservation', {
            'fields': ('game', 'slot', 'mail')
        }),
        ('Joueurs', {
            'fields': ('spectators',)
        })
    )


class ThemePriorityInline(admin.TabularInline):
    model = ThemePriority
    readonly_fields = ('priority',)


class GameAdmin(admin.ModelAdmin):

    inlines = [ThemePriorityInline, ]
    list_display = ('name', 'main_theme', 'vr')
    list_filter = ('name', 'vr')
    search_fields = ('name', )
    fieldsets = (
        ('Jeu', {
            'fields': ('name', 'vr',)
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


class ThemePriorityAdmin(admin.ModelAdmin):
    readonly_fields = ('priority',)

    def get_model_perms(self, request):
        return {}


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Spectator)
admin.site.register(Slot)
admin.site.register(Tarif)
admin.site.register(Theme)
admin.site.register(ThemePriority, ThemePriorityAdmin)
