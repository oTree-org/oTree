from django.contrib import admin
import ultimatum.models as models
import otree.adminlib as adminlib


class PlayerAdmin(adminlib.Particlayer):
    readonly_fields = adminlib.get_readonly_fields(models.Participantlayer_display = adminlib.get_list_display(models.Participant, realayerds)


class MatchAdmin(adminlib.MatchAdmin):
    readonly_fields = adminlib.get_readonly_fields(models.Match)
    list_display = adminlib.get_list_display(models.Match, readonly_fields)


class TreatmentAdmin(adminlib.TreatmentAdmin):
    readonly_fields = adminlib.get_readonly_fields(models.Treatment)
    list_display = adminlib.get_list_display(models.Treatment, readonly_fields)


class SubsessionAdmin(adminlib.SubsessionAdmin):
    readonly_fields = adminlib.get_readonly_fields(models.Subsession)
    list_display = adminlib.get_list_display(models.Subsession, readonly_fields)


admin.site.register(models.Participant, ParticipantAdmin)
admin.site.register(models.Match, MatchAdmin)
admin.site.register(models.Treatment, TreatmentAdmin)
admin.site.register(models.Subsession, SubsessionAdmin)
