from django.contrib.gis import admin
from tim.models import ModeratedProject
import reversion

class ModeratedProjectAdmin(reversion.VersionAdmin):
    # fieldsets = [
    #     (None, {'fields': ['name', 'removed', 'compl_date', 'area', 'redevelopment', 'location']}),
    #     ('Housing Developments', {'fields': ['hd_singlefam_units', 'hd_attached_units', 'hd_apt_units', 'hd_cluster', 'hd_over55', 'hd_mixeduse', 'zoning_tool']}),
    #     ('Economic Development', {'fields': ['ed_jobs', 'ed_sqft', 'ed_type']}),
    #     ('Review', {'fields': ['comments', 'confirmed', 'confirmed_by', 'located', 'located_by']}),   
    # ]
    # list_filter = ('complyr',)
    exclude = ('location',)
    list_display = ('ddname', 'municipality', 'last_modified', 'completed', 'approved', )
    search_fields = ['ddname','description',]


admin.site.register(ModeratedProject, ModeratedProjectAdmin)