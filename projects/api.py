from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from projects.models import Project, Taz
from projects.tastyhacks import GeoResource


class TazResource(ModelResource):
    """
    TAZ
    """
    class Meta:
        queryset = Taz.objects.all()
        allowed_methods = ['get',]
        fields = ['taz_id', 'town_id', 'town_name',]
        limit = 20
        filtering = {
            'taz_id': ALL,
            'town_id': ALL,
        }

class ProjectResource(GeoResource):
    """
    Project
    """

    taz = fields.ToOneField('projects.api.TazResource', 'taz', full=True)

    class Meta:
        queryset = Project.objects.transform(4326).all()
        allowed_methods = ['get',]
       # excludes = ['location',]
        filtering = {
            'name': ALL,
            'taz': ALL_WITH_RELATIONS,
            'status': ALL,
            'compl_date': ALL,
        }