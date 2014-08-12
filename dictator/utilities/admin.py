from django.contrib import admin
import dictator.models as models
import otree.adminlib as adminlib

class PlayerAdmin(adminlib.PlayerAdmin):
    readonly_fields = adminlib.get_callables(models.Player)
    list_display = adminlib.get_all_fields_for_table(models.Player, readonly_fields)

class MatchAdmin(adminlib.MatchAdmin):
    readonly_fields = adminlib.get_callables(models.Match)
    list_display = adminlib.get_all_fields_for_table(models.Match, readonly_fields)

class TreatmentAdmin(adminlib.TreatmentAdmin):
    readonly_fields = adminlib.get_callables(models.Treatment)
    list_display = adminlib.get_all_fields_for_table(models.Treatment, readonly_fields)

class SubsessionAdmin(adminlib.SubsessionAdmin):
    readonly_fields = adminlib.get_callables(models.Subsession)
    list_display = adminlib.get_all_fields_for_table(models.Subsession, readonly_fields)

admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Match, MatchAdmin)
admin.site.register(models.Treatment, TreatmentAdmin)
admin.site.register(models.Subsession, SubsessionAdmin)
