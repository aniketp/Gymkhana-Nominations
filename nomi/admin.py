from django.contrib import admin
from .models import Nomination, NominationInstance, UserProfile, Post, Club


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_no', 'year', 'programme', 'department', 'hall', 'room_no')

admin.site.register(UserProfile, UserProfileAdmin)


class NominationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'results_declared')

admin.site.register(Nomination, NominationAdmin)


class NominationInstanceAdmin(admin.ModelAdmin):
    list_display = ('nomination', 'user', 'status')

admin.site.register(NominationInstance, NominationInstanceAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_name', 'club', 'parent')

admin.site.register(Post, PostAdmin)


class ClubAdmin(admin.ModelAdmin):
    list_display = ('club_name', 'club_parent')

admin.site.register(Club, ClubAdmin)