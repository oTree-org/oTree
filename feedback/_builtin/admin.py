# This file is auto-generated.

from django.contrib import admin
from .. import models
import otree.adminlib as adminlib

class PlayerAdmin(adminlib.PlayerAdmin):
    readonly_fields = adminlib.get_callables(models.Player)
    list_display = adminlib.get_all_fields_for_table(models.Player, readonly_fields)

class GroupAdmin(adminlib.GroupAdmin):
    readonly_fields = adminlib.get_callables(models.Group)
    list_display = adminlib.get_all_fields_for_table(models.Group, readonly_fields)

class SubsessionAdmin(adminlib.SubsessionAdmin):
    readonly_fields = adminlib.get_callables(models.Subsession)
    list_display = adminlib.get_all_fields_for_table(models.Subsession, readonly_fields)

admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.Subsession, SubsessionAdmin)
