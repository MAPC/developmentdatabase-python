from communitycomments.accounts.models import UserProfile
from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user','town', 'position']
    list_display = ('user', 'full_name', 'town', 'position')

admin.site.register(UserProfile, UserProfileAdmin)