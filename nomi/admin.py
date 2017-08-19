from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_no', 'programme', 'department', 'hall', 'room_no')

admin.site.register(UserProfile, UserProfileAdmin)


class NominationAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'opening_date', 'deadline')

admin.site.register(Nomination, NominationAdmin)


class NominationInstanceAdmin(admin.ModelAdmin):
    list_display = ('nomination', 'user', 'status')

admin.site.register(NominationInstance, NominationInstanceAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_name','pk', 'club', 'parent')

admin.site.register(Post, PostAdmin)


class ClubAdmin(admin.ModelAdmin):
    list_display = ('pk', 'club_name', 'club_parent')

admin.site.register(Club, ClubAdmin)


class PostHistoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'start', 'end')

admin.site.register(PostHistory, PostHistoryAdmin)



admin.site.register(Deratification)


admin.site.register(GroupNomination)
admin.site.register(ReopenNomination)
admin.site.register(Session)
