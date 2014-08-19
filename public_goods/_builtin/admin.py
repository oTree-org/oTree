from django.contrib import admin
import public_goods.models as models
import otree.adminlib as adminlib

class PlayerAdmin(adminlib.PlayerAdmin):
    readonly_fields = adminlib.get_readonly_fields(models.Player)
    list_display = adminlib.get_list_display(models.Player, readonly_fields)

class MatchAdmin(adminlib.MatchAdmin):
    readonly_fields = adminlib.get_readonly_fields(models.Match)
    list_display = adminlib.get_list_display(models.Match, readonly_fields)

class TreatmentAdmin(adminlib.TreatmentAdmin):
    readonly_fields = adminlib.get_readonly_fields(models.Treatment)
    list_display = adminlib.get_list_display(models.Treatment, readonly_fields)

class SubsessionAdmin(adminlib.SubsessionAdmin):
    readonly_fields = adminlib.get_readonly_fields(models.Subsession)
    list_display = adminlib.get_list_display(models.Subsession, readonly_fields)

admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Match, MatchAdmin)
admin.site.register(models.Treatment, TreatmentAdmin)
admin.site.register(models.Subsession, SubsessionAdmin)
