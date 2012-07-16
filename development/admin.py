from django.contrib.gis import admin

from development.models import Project, Taz, Municipality, CommunityType, ProjectStatus, ZoningTool, ProjectType

import reversion

# default GeoAdmin overloads
admin.GeoModelAdmin.default_lon = -7915039
admin.GeoModelAdmin.default_lat = 5216500 
admin.GeoModelAdmin.default_zoom = 10

class ProjectAdmin(reversion.VersionAdmin):
    # fieldsets = [
    #     (None, {'fields': ['name', 'removed', 'compl_date', 'area', 'redevelopment', 'location']}),
    #     ('Housing Developments', {'fields': ['hd_singlefam_units', 'hd_attached_units', 'hd_apt_units', 'hd_cluster', 'hd_over55', 'hd_mixeduse', 'zoning_tool']}),
    #     ('Economic Development', {'fields': ['ed_jobs', 'ed_sqft', 'ed_type']}),
    #     ('Review', {'fields': ['comments', 'confirmed', 'confirmed_by', 'located', 'located_by']}),   
    # ]
    # list_filter = ('complyr',)
    exclude = ('location',)
    list_display = ('ddname', 'municipality', 'last_modified', 'projecttype', 'status', 'complyr', 'prjacrs', )
    search_fields = ['ddname','description',]
    

class TazAdmin(admin.OSMGeoAdmin):
	list_display = ('taz_id','municipality')
	fieldsets = (
       (None, {'fields': (('taz_id','municipality',))}),
       ('Map', {'fields': ('geometry',)}),
     )
	search_fields = ['taz_id']


admin.site.register(Project, ProjectAdmin) 
admin.site.register(Taz, TazAdmin)
admin.site.register(Municipality, admin.OSMGeoAdmin) 
admin.site.register(CommunityType, admin.ModelAdmin)
admin.site.register(ProjectStatus, admin.ModelAdmin)
admin.site.register(ZoningTool, admin.ModelAdmin)
admin.site.register(ProjectType, admin.ModelAdmin)