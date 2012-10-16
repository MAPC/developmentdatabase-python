from tastypie.contrib.gis.resources import ModelResource
from tastypie import fields
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie.cache import SimpleCache

from development.models import Project, Taz, Municipality, ProjectStatus


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
        cache = SimpleCache()
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
        cache = SimpleCache()
        filtering = {
            'taz_id': ALL,
            'municipality': ALL,
        }

class ProjectStatusResource(ModelResource):
    class Meta:
        queryset = ProjectStatus.objects.all()
        allowed_methods = ['get']
        include_resource_uri = False
        cache = SimpleCache()
        filtering = {
            'name': ALL
        }


class ProjectResource(ModelResource):
    """
    Project
    """

    taz = fields.ToOneField('development.api.TazResource', 'taz', full=True)
    status = fields.ToOneField('development.api.ProjectStatusResource', 'status')

    class Meta:
        queryset = Project.objects.transform(4326).filter(removed=False, draft=False)
        allowed_methods = ['get']
        # fields = ['ddname', 'projecttype', 'status', 'complyr', 'tothu', 'ovr55', 'pctaffall', 'totemp', 'last_modified', ]
        include_absolute_url = True
        include_resource_uri = False
        authorization = Authorization()
        ordering = ['last_modified', ]
        # cache = SimpleCache()
        filtering = {
            'dd_id': ALL,
            'ddname': ALL,
            'complyr': ALL,
            'ovr55': ALL,
            'projecttype': ALL, 
            'status': ALL,
            'tothu': ALL,  
            'pctaffall': ALL, 
            'totemp': ALL,
            'taz': ALL_WITH_RELATIONS, 
        }

        