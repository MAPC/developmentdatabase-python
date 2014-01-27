from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db.models.loading import get_model

from django.conf import settings
from django.utils.dateparse import parse_datetime

from model_utils.managers import InheritanceManager

import pytz
import requests
import reversion

# south introspection rules
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.PointField'])
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.MultiPolygonField'])
except ImportError:
    pass

def user_new_unicode(self):
    return self.username if self.get_full_name() == "" else self.get_full_name()

# Replace the __unicode__ method in the User class with out new implementation
User.__unicode__ = user_new_unicode 

class CommunityType(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Subregion(models.Model):
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('Subregion')
        verbose_name_plural = _('Subregions')
        ordering = ['abbr']

    def __unicode__(self):
        return self.abbr
    

class Municipality(models.Model):
    muni_id       = models.IntegerField('Municipality ID', primary_key=True)
    name          = models.CharField('Municipality Name', max_length=50, unique=True)
    communitytype = models.ForeignKey(CommunityType, blank=True, null=True)
    subregion     = models.ForeignKey(Subregion, null=True)
    
    geometry      = models.MultiPolygonField(srid=26986)
    objects       = models.GeoManager()
    
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
    
    taz_id       = models.IntegerField(primary_key=True)
    municipality = models.ForeignKey(Municipality)
    
    geometry     = models.MultiPolygonField(srid=26986)
    objects      = models.GeoManager()
    
    class Meta:
        verbose_name=u'TAZ'
        verbose_name_plural = 'TAZs'
        ordering = ['taz_id']
    
    def __unicode__(self):
        return "%s - %s" % (self.taz_id, self.municipality)


class ZipCode(models.Model):
    """
    Massachusetts Zip Codes, used for approx. geocoding
    """

    zipcode  = models.CharField(max_length=5)
    name     = models.CharField(max_length=100)
    state    = models.CharField(max_length=2)

    geometry = models.MultiPolygonField(srid=26986)
    objects  = models.GeoManager()

    class Meta:
        verbose_name = _('ZipCode')
        verbose_name_plural = _('ZipCodes')
        ordering = ['zipcode']

    def __unicode__(self):
        return self.zipcode

    @property
    def address(self):
        """ Returns formatting to fit in street addresses """
        return '%s, %s %s' % (self.name, self.state, self.zipcode)
    


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
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order']


class WalkScore(models.Model):
    """ Model class according to http://www.walkscore.com/professional/api.php """

    status      = models.IntegerField()
    walkscore   = models.IntegerField()
    description = models.CharField(max_length=100)
    updated     = models.DateTimeField()
    ws_link     = models.URLField()
    snapped_lat = models.FloatField()
    snapped_lon = models.FloatField()

    geometry    = models.PointField(geography=True, null=True)
    objects     = models.GeoManager() 

    class Meta:
        verbose_name = _('WalkScore')
        verbose_name_plural = _('WalkScores')

    def __unicode__(self):
        return '%i (%s)' % (self.walkscore, self.description)

    def save(self, *args, **kwargs):
        try:
            self.geometry = Point(self.snapped_lon, self.snapped_lat)
        except:
            self.geometry = None        
        super(WalkScore, self).save(*args, **kwargs)
    

class TODStation(models.Model):
    """ Adjusted buffer around transit stations """

    station_id = models.IntegerField()
    station_name = models.CharField(max_length=50)
    subway = models.BooleanField()
    comrail = models.BooleanField()
    taz = models.ForeignKey(Taz)

    geometry = models.MultiPolygonField(srid=26986)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('TODStation')
        verbose_name_plural = _('TODStations')
        ordering = ['station_name', ]


    def __unicode__(self):
        return self.station_name.title()


class Parcel(models.Model):
    """
    A distinct plot of land
    """

    gid          = models.AutoField(primary_key=True)
    parcel_id    = models.IntegerField(null=True)
    geometry     = models.MultiPolygonField(srid=26986, null=True)
    objects      = models.GeoManager()
    municipality = models.ForeignKey(Municipality, null=True)
    # taxloc_id    = models.CharField('Tax Loc ID', max_length=18, null=True)
    parloc_id    = models.CharField('Parcel Loc ID', max_length=18, null=True)
    loc_id_cnt   = models.IntegerField('Loc ID Count', null=True)
    land_value   = models.FloatField('Land Value', null=True)
    bldg_value   = models.FloatField('Building Value', null=True)
    othr_value   = models.FloatField('Other Value', null=True)
    total_valu   = models.FloatField('Total Value', null=True)
    ls_price     = models.FloatField('List Price', null=True)
    ls_date      = models.CharField('List Date', max_length=8, null=True)
    bldg_area    = models.FloatField('Building Area', null=True)
    res_area     = models.FloatField('Residential Area', null=True)
    luc_1        = models.CharField('Field Description', max_length=4, null=True)
    luc_2        = models.CharField('Field Description', max_length=4, null=True)
    # luc_adjust   = models.CharField('Field Description', max_length=5, null=True)
    # units_num    = models.FloatField('Number of Units', null=True)
    # rooms_num    = models.FloatField('Number of Rooms', null=True)
    # zoning       = models.CharField('Zoning', max_length=8, null=True)
    # style        = models.CharField('Architectural Style', max_length=20, null=True)
    yr_built     = models.IntegerField('Year Built', null=True)
    site_addr    = models.CharField('Site Address', max_length=80, null=True)
    addr_str     = models.CharField('Site Street Address', max_length=60, null=True)
    addr_num     = models.CharField('Site Number on Street', max_length=12, null=True)
    addr_zip     = models.CharField('Site Zip Code', max_length=10, null=True)
    owner_name   = models.CharField('Owner Name', max_length=80, null=True)
    owner_addr   = models.CharField('Owner Street Address', max_length=80, null=True)
    owner_city   = models.CharField('Owner City', max_length=25, null=True)
    owner_stat   = models.CharField('Owner State', max_length=2, null=True)
    owner_zip    = models.CharField('Owner Zip Code', max_length=10, null=True)
    fy           = models.IntegerField('Fiscal Yearmpy ', null=True)
    lot_areaft   = models.FloatField('Lot Area in Feet', null=True)
    far          = models.FloatField('Floor Area Ratio', null=True)

    def owner_data(self):
        name  = self.owner_name or ''
        addr  = self.owner_addr or ''
        city  = self.owner_city or ''
        state = self.owner_stat or ''
        zipc  = self.owner_zip  or ''
        return name + " " + addr + " " + city + " " + state + " " + zipc        


    class Meta:
        verbose_name = _('Parcel')
        verbose_name_plural = _('Parcels')
        ordering = ['gid', ]

    def __unicode__(self):
        return self.taxloc_id


class DisplayProjectManager(models.GeoManager):
    def get_query_set(self):
        moderated_project = get_model('tim','ModeratedProject')
        return super(DisplayProjectManager, self).get_query_set().exclude(status__name='Conceptual').exclude( dd_id__in=[m.dd_id for m in moderated_project.objects.all()] )


class Project(models.Model):
    """
    An economic or housing development project.
    """

    dd_id      = models.AutoField(primary_key=True)
    taz        = models.ForeignKey(Taz, blank=True, null=True, editable=False)
    ddname     = models.CharField('Project Name', max_length=100)
    status     = models.ForeignKey(ProjectStatus)
    complyr    = models.IntegerField('Year of Completion', null=True, help_text='Estimated or actual.')
    prjacrs    = models.FloatField('Project Area', null=True, help_text='In acres.')
    rdv        = models.NullBooleanField('Redevelopment', blank=True, null=True)
    
    singfamhu  = models.IntegerField('Single Family Housing', blank=True, null=True, help_text='Number of units.')
    twnhsmmult = models.IntegerField('Townhouse and Small Multifamily', blank=True, null=True, help_text='Number of units.')
    lgmultifam = models.IntegerField('Large Multifamily', blank=True, null=True, help_text='Number of units.')
    tothu      = models.FloatField('Total Housing', null=True, help_text='Number of units.')
    gqpop      = models.IntegerField('Group Quarters', blank=True, null=True, help_text='Number of beds.')
    pctaffall  = models.FloatField('Affordable Units', blank=True, null=True, help_text='In percent.')
    clustosrd  = models.NullBooleanField('Cluster Subdivision', blank=True, null=True)
    ovr55      = models.NullBooleanField('Age Restricted', blank=True, null=True)
    mxduse     = models.NullBooleanField('Mixed Use', blank=True, null=True)
    ch40       = models.ForeignKey(ZoningTool, blank=True, null=True, verbose_name='Zoning Tool')

    # Nonresidential Development Fields
    rptdemp    = models.FloatField('Reported Employment', blank=True, null=True)
    emploss    = models.FloatField('Employment Loss', blank=True, null=True)
    totemp     = models.FloatField('Est. employment', blank=True, null=True)
    commsf     = models.FloatField('Total Non-Residential Development', null=True, help_text='In square feet.')
    retpct     = models.FloatField('Retail / Restaurant Percentage', blank=True, null=True, help_text='In percent.')
    ofcmdpct   = models.FloatField('Office / Medical Percentage', blank=True, null=True, help_text='In percent.')
    indmfpct   = models.FloatField('Manufacturing / Industrial Percentage', blank=True, null=True, help_text='In percent.')
    whspct     = models.FloatField('Warehouse / Trucking Percentage', blank=True, null=True, help_text='In percent.')
    rndpct     = models.FloatField('Lab / R & D  Percentage', blank=True, null=True, help_text='In percent.')
    edinstpct  = models.FloatField('Edu / Institution Percentage)', blank=True, null=True, help_text='In percent.')
    othpct     = models.FloatField('Other Non-Residential Percentage', blank=True, null=True, help_text='In percent.')
    hotelrms   = models.FloatField('Hotel Rooms', blank=True, null=True)

    mfdisc     = models.FloatField('Metro Future Discount', blank=True, null=True, help_text='In percent.')
    projecttype_detail = models.TextField('Project Type Detail', blank=True, null=True)
    
    description  = models.TextField('description', blank=True, null=True)
    url          = models.URLField('Project Website', blank=True, null=True, verify_exists=False)
    mapcintrnl   = models.TextField('MAPC Internal Comments', blank=True, null=True)
    otheremprat2 = models.FloatField('Multiplier for Other Square Footage', blank=True, null=True)

    projecttype  = models.ForeignKey(ProjectType, null=True)
    stalled      = models.BooleanField('Stalled')
    phased       = models.BooleanField('Phased')
    dev_name     = models.CharField('Developer Name', blank=True, null=True, max_length=100)
    url_add      = models.URLField('Additional Website', blank=True, null=True, verify_exists=False)
    affordable_comment = models.TextField('Affordability Comment', blank=True, null=True)
    parking_spaces     = models.IntegerField('Parking Spaces', blank=True, null=True)
    as_of_right  = models.NullBooleanField('As Of Right', blank=True, null=True)
    walkscore    = models.ForeignKey(WalkScore, null=True, blank=True)
    todstation   = models.ForeignKey(TODStation, null=True, blank=True, verbose_name=u'TOD Station')
    total_cost   = models.IntegerField('Total Cost', blank=True, null=True)
    total_cost_allocated_pct = models.FloatField('Funding Allocated', blank=True, null=True, help_text='In percent.')
    draft        = models.BooleanField(help_text='Required project information is incomplete.')
    removed      = models.BooleanField(help_text='Deleted project, will not be shown on public page')    

    parcel       = models.ForeignKey(Parcel, null=True, blank=True)

    # internal
    created_by       = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='project_created_by')
    created          = models.DateTimeField(auto_now_add=True)
    last_modified_by = models.ForeignKey(User, editable=False, blank=True, null=True, related_name='project_last_modified_by')
    last_modified    = models.DateTimeField(auto_now=True)

    # tmp
    xcoord = models.FloatField(blank=True, null=True)
    ycoord = models.FloatField(blank=True, null=True)

    # geometry
    location = models.PointField(srid=26986, blank=True, null=True) # SRS mass state plane
    objects  = models.GeoManager()
    display  = DisplayProjectManager()

    # Calculated Fields
    est_employment = models.FloatField('MAPC Estimated Employment Potential', null=True)
    
    class Meta:
        ordering = ['dd_id', ]

    def save(self, *args, **kwargs):

        # record user
        user = kwargs.pop('user', None)
        self.last_modified_by = user

        # TODO: Ripe for refactoring & metaprogramming
        # set TAZ
        try:
            self.taz = Taz.objects.get(geometry__contains=self.location)
        except Taz.DoesNotExist:
            self.taz = None 

        # set TOD Station
        try:
            self.todstation = TODStation.objects.get(geometry__contains=self.location)
        except TODStation.DoesNotExist:
            self.todstation = None
        
        # set Parcel
        try:
            self.parcel = Parcel.objects.get(geometry__contains=self.location)
        except Parcel.MultipleObjectsReturned:
            self.parcel = Parcel.objects.filter(geometry__contains=self.location)[0]
        except Parcel.DoesNotExist:
            self.parcel = None

        # estimate employment
        self.est_employment = self.estimate_employment()


        # the free walkscore api is limited to 1000 requests per day
        # update walkscore only on new or moved projects
        udate_walkscore = kwargs.pop('update_walkscore', False)
        if udate_walkscore == True:
            # get walkscore
            try:
                self.walkscore = self.get_walkscore()
            except:
                pass

        super(Project, self).save(*args, **kwargs)


    def clean(self):
        from django.core.exceptions import ValidationError

        retail    = self.retpct    or 0.0
        office    = self.ofcmdpct  or 0.0
        manuf     = self.indmfpct  or 0.0
        warehouse = self.whspct    or 0.0
        labrnd    = self.rndpct    or 0.0
        education = self.edinstpct or 0.0
        other     = self.othpct    or 0.0
        total_pct = (retail + office + manuf + warehouse + labrnd + education + other)
        
        if total_pct > 1.0:
            raise ValidationError('Floor space use percentages may not equal more than 1.')


    def __unicode__(self):
        return "%s (%s)" % (self.ddname, self.dd_id)

    def name(self):
        return self.ddname
        
    def municipality(self):
        return self.taz.municipality

    def get_zipcode(self):
        try:
            zipcode = ZipCode.objects.get(geometry__contains=self.location)
        except ZipCode.DoesNotExist:
            zipcode = None
        return zipcode

    def parcel_address(self):
        if self.parcel != None:
            if self.get_zipcode != None:
                site_address   = self.parcel.site_addr or ''
                city_state_zip = ", " + self.get_zipcode().address or ''
                return site_address + city_state_zip

    def estimate_employment(self):
        categories = [
            'retail_restaurant',
            'office_med',
            'manuf_indust',
            'warehouse_trucking',
            'lab_rd',
            'edu_inst',
            'other_nonres'
        ]

        category_fields = {
            'retail_restaurant':  'retpct',
            'office_med':         'ofcmdpct',
            'manuf_indust':       'indmfpct',
            'warehouse_trucking': 'whspct',
            'lab_rd':             'rndpct',
            'edu_inst':           'edinstpct',
            'other_nonres':       'othpct',
        }

        field_values = {
            'retpct':    self.retpct,
            'ofcmdpct':  self.ofcmdpct,
            'indmfpct':  self.indmfpct,
            'whspct':    self.whspct,
            'rndpct':    self.rndpct,
            'edinstpct': self.edinstpct,
            'othpct':    self.othpct,
        }

        category_multipliers = {
            'retail_restaurant':  750,
            'office_med':         330,
            'manuf_indust':       500,
            'warehouse_trucking': 750,
            'lab_rd':             330,
            'edu_inst':           330,
            'other_nonres':       self.otheremprat2,
            'hotel':              0.5
        }

        total_nonres_sqft = self.commsf

        estimated_employment = 0

        for category in categories:
            field_name = category_fields[category]
            if field_name != None:
                percent_category  = field_values[field_name] or 0
                employee_per_sqft = category_multipliers[category] or 0
                sqft_per_employee = 0 
                if employee_per_sqft > 0:
                    sqft_per_employee = 1.0 / employee_per_sqft
                try:
                    estimated_employment += ((total_nonres_sqft * percent_category) * sqft_per_employee)
                except TypeError:
                    pass

        estimated_employment += (self.hotelrms or 0) * category_multipliers['hotel']

        if estimated_employment == 0:
            return None
        else:
            try:
                return int(estimated_employment)
            except:
                return None

    @models.permalink
    def get_absolute_url(self):
        return ('development.views.detail', None, { 'dd_id': self.dd_id, })

    def get_verbose_field_name(self, field):
        return self._meta.get_field_by_name(field)[0].verbose_name

    def get_walkscore(self):
        """ 
        Gets walkscore from API, limited to 1000 requests per day 
        Example response:
        {
            "status": 1,
            "walkscore": 38,
            "description": "Car-Dependent",
            "updated": "2012-08-13 19:00:20.819797",
            "logo_url": "http://www2.walkscore.com/images/api-logo.gif",
            "more_info_icon": "http://www2.walkscore.com/images/api-more-info.gif",
            "more_info_link": "http://www.walkscore.com/how-it-works.shtml",
            "ws_link": "http://www.walkscore.com/score/Boxborough-MA-01719/lat=42.480611424525264/lng=-71.516146659851088/?utm_source=mapc.org&utm_medium=ws_api&utm_campaign=ws_api",
            "snapped_lat": 42.4800,
            "snapped_lon": -71.5155
        }
        """

        point = self.location
        point.transform(4326)
        address = ''
        zipcode = self.get_zipcode()
        if zipcode:
            address = zipcode.address

        ws_params = {
            'format': 'json', 
            'address': address, 
            'lat': point.y, 
            'lon': point.x, 
            'wsapikey': settings.WSAPIKEY
        }
        ws_request = requests.get('http://api.walkscore.com/score', params=ws_params)

        ws_json = ws_request.json()

        # check if we have good response
        if ws_json['status'] == 1:
            walkscore = WalkScore.objects.get_or_create(
                status = ws_json['status'],
                walkscore = ws_json['walkscore'],
                description = ws_json['description'],
                updated = pytz.UTC.localize(parse_datetime(ws_json['updated'])), # assume UTC
                ws_link = ws_json['ws_link'],
                snapped_lat = ws_json['snapped_lat'],
                snapped_lon = ws_json['snapped_lon']
            )
            return walkscore[0]
        else:
            return None


reversion.register(Project)
