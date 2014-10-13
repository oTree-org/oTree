from django.contrib import admin
from .. import models
import otree.adminlib as adminlib

class PlayerAdmin(adminlib.PlayerAdmin):
    readonly_fields = adminlib.get_readonly_fields(models.Player)
    list_display = adminlib.get_list_display(models.Player, readonly_fields)

class GroupAdmin(adminlib.GroupAdmin):
    readonly_fields = adminlib.get_readonly_fields(models.Group)
    list_display = adminlib.get_list_display(models.Group, readonly_fields)

class SubsessionAdmin(adminlib.SubsessionAdmin):
    readonly_fields = adminlib.get_readonly_fields(models.Subsession)
    list_display = adminlib.get_list_display(models.Subsession, readonly_fields)

admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.Subsession, SubsessionAdmin)
