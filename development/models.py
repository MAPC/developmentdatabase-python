from django.contrib.gis.db import models
from django.contrib.auth.models import User


# south introspection rules
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.PointField'])
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.MultiPolygonField'])
except ImportError:
    pass

class CommunityType(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Municipality(models.Model):
    muni_id = models.IntegerField('Municipality ID', primary_key=True)
    name = models.CharField('Municipality Name', max_length=50, unique=True)
    communitytype = models.ForeignKey(CommunityType, blank=True, null=True)
    
    geometry = models.MultiPolygonField(srid=26986)
    objects = models.GeoManager()
    
    class Meta:
        verbose_name_plural = 'Municipalities'
        ordering = ['name']
    
    def __unicode__(self):
        return self.name


class Taz(models.Model):
    """ 
    Transportation Analysis Zone, 
    smaller regional units than towns. 
    """
    
    taz_id = models.IntegerField(primary_key=True)
    municipality = models.ForeignKey(Municipality)
    
    geometry = models.MultiPolygonField(srid=26986)
    objects = models.GeoManager()
    
    class Meta:
        verbose_name=u'TAZ'
        verbose_name_plural = 'TAZs'
        ordering = ['taz_id']
    
    def __unicode__(self):
        return "%s - %s" % (self.taz_id, self.municipality)


class ProjectStatus(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Project statuses'

    def __unicode__(self):
        return self.name
    
class ZoningTool(models.Model):
    name = models.CharField('Zoning Tool', max_length=3)

    def __unicode__(self):
        return self.name


class ProjectType(models.Model):
    name = models.CharField('Project Type', max_length=100)

    def __unicode__(self):
        return self.name

    
class Project(models.Model):
    """
    An economic or housing development project.
    """

    dd_id = models.AutoField(primary_key=True)
    taz = models.ForeignKey(Taz, blank=True, null=True, editable=False)
    ddname = models.CharField('Project Name', max_length=100)
    status = models.ForeignKey(ProjectStatus)
    complyr = models.IntegerField('Year of Completion', null=True, help_text='Estimated or actual.')
    prjacrs = models.FloatField('Project Area', null=True, blank=True, help_text='In acres.')
    rdv = models.NullBooleanField('Redevelopment', blank=True, null=True)
    
    singfamhu = models.IntegerField('Single Family Housing', blank=True, null=True, help_text='Number of units.')
    twnhsmmult = models.IntegerField('Townhouse and Small Multifamily', blank=True, null=True, help_text='Number of units.')
    lgmultifam = models.IntegerField('Large Multifamily', blank=True, null=True, help_text='Number of units.')
    tothu = models.FloatField('Total Housing', null=True, help_text='Number of units.')
    gqpop = models.IntegerField('Group Quarters', blank=True, null=True, help_text='Number of beds.')
    pctaffall = models.FloatField('Affordable Units', blank=True, null=True, help_text='In percent.')
    clustosrd = models.NullBooleanField('Cluster Subdivision', blank=True, null=True)
    ovr55 = models.NullBooleanField('Age Restricted', blank=True, null=True)
    mxduse = models.NullBooleanField('Mixed Use', blank=True, null=True)
    ch40 = models.ForeignKey(ZoningTool, blank=True, null=True)

    rptdemp = models.FloatField('Reported Employment', blank=True, null=True)
    emploss = models.FloatField('Employment Loss', blank=True, null=True)
    totemp = models.FloatField('Total Employment', blank=True, null=True)
    commsf = models.FloatField('Total Non-Residential Development', null=True, help_text='In square feet.')
    retpct = models.FloatField('Retail / Restaurant Percentage', blank=True, null=True, help_text='In percent.')
    ofcmdpct = models.FloatField('Office / Medical Percentage', blank=True, null=True, help_text='In percent.')
    indmfpct = models.FloatField('Manufacturing / Industrial Percentage', blank=True, null=True, help_text='In percent.')
    whspct = models.FloatField('Warehouse / Trucking Percentage', blank=True, null=True, help_text='In percent.')
    rndpct = models.FloatField('Lab / R & D  Percentage', blank=True, null=True, help_text='In percent.')
    edinstpct = models.FloatField('Edu / Institution Percentage)', blank=True, null=True, help_text='In percent.')
    othpct = models.FloatField('Other', blank=True, null=True, help_text='In percent.')
    hotelrms = models.FloatField('Hotel Rooms', blank=True, null=True)

    mfdisc = models.FloatField('Metro Future Discount', blank=True, null=True, help_text='In percent.')
    projecttype_detail = models.TextField('Project Type Detail', blank=True, null=True)
    
    description = models.TextField('description', blank=True, null=True)
    url = models.URLField('Project Website', blank=True, null=True, verify_exists=False)
    mapcintrnl = models.TextField('MAPC Internal Comments', blank=True, null=True)
    otheremprat2 = models.FloatField(blank=True, null=True)

    # new
    projecttype = models.ForeignKey(ProjectType, blank=True, null=True)
    stalled = models.BooleanField('Stalled')
    phased = models.BooleanField('Phased')
    dev_name = models.CharField('Developer Name', blank=True, null=True, max_length=100)
    url_add = models.URLField('Additional Website', blank=True, null=True, verify_exists=False)
    affordable_comment = models.TextField('Affordability Comment', blank=True, null=True)
    parking_spaces = models.IntegerField('Parking Spaces', blank=True, null=True)
    as_of_right = models.NullBooleanField('As Of Right', blank=True, null=True)
    walkscore = models.IntegerField('WalkScore', blank=True, null=True)
    total_cost = models.IntegerField('Total Cost', blank=True, null=True)
    total_cost_allocated_pct = models.FloatField('Funding Allocated', blank=True, null=True, help_text='In percent.')
    draft = models.BooleanField(help_text='Required project information is incomplete.')
    removed = models.BooleanField(help_text='Deleted project, will not be shown on public page')    

    # internal
    created_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='project_created_by')
    created = models.DateTimeField(auto_now_add=True)
    last_modified_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='project_last_modified_by')
    last_modified = models.DateTimeField(auto_now=True)

    # tmp
    xcoord = models.FloatField(blank=True, null=True)
    ycoord = models.FloatField(blank=True, null=True)

    # geometry
    location = models.PointField(srid=26986, blank=True, null=True) # SRS mass state plane
    objects = models.GeoManager()
    
    class Meta:
        ordering = ['dd_id', ]

    def save(self, *args, **kwargs):
        try:
            # find and cache TAZ for project location
            self.taz = Taz.objects.get(geometry__contains=self.location)
        except:
            self.taz = None        
        super(Project, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.ddname
    
    def municipality(self):
        return self.taz.municipality.name

    @models.permalink
    def get_absolute_url(self):
        return ('development.views.detail', None, { 'dd_id': self.dd_id, })

    def get_verbose_field_name(self, field):
        return self._meta.get_field_by_name(field)[0].verbose_name
