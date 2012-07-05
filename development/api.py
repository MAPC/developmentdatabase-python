from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization

from development.models import Project, Taz, Municipality
from development.tastyhacks import GeoResource


class MuniResource(ModelResource):
    """
    A town containing at least one Project
    """
    class Meta:
        queryset = Municipality.objects.filter(taz__project__isnull=False).distinct('muni_id')
        allowed_methods = ['get', ]
        fields = ['town_id', 'name', ]
        include_resource_uri = False
        ordering = ['name', ]
        filtering = {
            'muni_id': ALL,
            'name': ALL,
        }


class TazResource(ModelResource):
    """
    TAZ containing at least one project
    """

    municipality = fields.ToOneField('development.api.MuniResource', 'municipality', full=True)

    class Meta:
        queryset = Taz.objects.filter(project__isnull=False).distinct('taz_id')
        allowed_methods = ['get',]
        fields = ['taz_id', 'municipality', ]
        include_resource_uri = False
        filtering = {
            'taz_id': ALL,
            'municipality': ALL,
        }


class ProjectResource(GeoResource):
    """
    Project
    """

    taz = fields.ToOneField('development.api.TazResource', 'taz', full=True)

    class Meta:
        queryset = Project.objects.transform(4326).all()
        allowed_methods = ['get', 'post']
        fields = ['location', 'name', 'p_type', 'status', 'completion', 'total_housing_units', 'age_restricted_pct', 'affordable_pct', 'jobs', ]
        include_absolute_url = True
        include_resource_uri = False
        authorization = Authorization()
        filtering = {
            'dd_id': ALL,
            'name': ALL,
            'completion': ALL,
            'age_restricted_pct': ALL,
            'p_type': ALL, 
            'status': ALL,
            'total_housing_units': ALL,  
            'affordable_pct': ALL, 
            'jobs': ALL,
            'taz': ALL_WITH_RELATIONS, 
        }