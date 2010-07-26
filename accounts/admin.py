from communitycomments.accounts.models import UserProfile
from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user','municipality', 'position']

admin.site.register(UserProfile, UserProfileAdmin)