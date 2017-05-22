from django.contrib import admin
from .models import Nomination, NominationInstance


class NominationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

admin.site.register(Nomination, NominationAdmin)


class NominationInstanceAdmin(admin.ModelAdmin):
    list_display = ('nomination', 'user', 'status')

admin.site.register(NominationInstance, NominationInstanceAdmin)