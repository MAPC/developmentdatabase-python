from communitycomments.projects.models import Project, Taz
# from django.contrib import admin
from django.contrib.gis import admin

class ProjectAdmin(admin.GeoModelAdmin):
    fieldsets = [
        (None, {'fields': ['taz', 'name', 'status', 'compl_date', 'area', 'redevelopment', 'location']}),
        ('Housing Developments', {'fields': ['hd_singlefam_units', 'hd_attached_units', 'hd_apt_units', 'hd_cluster', 'hd_over55', 'hd_mixeduse', 'hd_40b']}),
        ('Economic Development', {'fields': ['ed_jobs', 'ed_sqft', 'ed_type']}),
        ('Review', {'fields': ['comments', 'confirmed', 'confirmed_by', 'located', 'located_by']}),   
    ]
    list_display = ('name', 'taz', 'located', 'confirmed')
    list_filter = ['status']
    date_hierarchy = 'last_modified'
    search_fields = ['comments']
    
admin.site.register(Project, ProjectAdmin)

class TazAdmin(admin.GeoModelAdmin):
     list_display = ('taz_id','town_name')
     fieldsets = (
       (None, {'fields': (('taz_id','town_id','town_name'))}),
       ('Map', {'fields': ('geometry',)}),
     )
 
admin.site.register(Taz, TazAdmin)