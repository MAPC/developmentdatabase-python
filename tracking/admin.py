from django.contrib import admin
from tracking.models import Note

class NoteAdmin(admin.ModelAdmin):
    list_display = ('town_name', 'type', 'excerpt', 'action', 'attachment_name', 'last_modified')
    list_filter = ['type', 'action']
    search_fields = ['town__town_name', 'desc']
    
admin.site.register(Note, NoteAdmin) 