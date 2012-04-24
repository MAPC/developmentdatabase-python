from django.contrib.auth.models import User
from django.contrib.gis.db import models
# from django import forms
from django.forms import ModelForm, Textarea, HiddenInput

import datetime
from django.core.exceptions import ValidationError
# required for finding taz for project location
# from django.contrib.gis.geos import *

from django.template import RequestContext
#from django.core.management.validation import max_length

# Create your models here.

    
class Town(models.Model):
    town_id = models.IntegerField('Municipality ID', unique=True)
    town_name = models.CharField('Municipality Name', max_length=50, unique=True)
    type = models.CharField(max_length=10)
    
    # GeoDjango-specific: a geometry field and overriding 
    # the default manager with a GeoManager instance.
    geometry = models.MultiPolygonField(srid=26986)
    objects = models.GeoManager()
    
    # So the model is pluralized correctly in the admin.
    class Meta:
        verbose_name_plural = 'Towns'
        ordering = ['town_name']
    
    # Returns the string representation of the model.
    def __unicode__(self):
        return self.town_name


class Taz(models.Model):
    """ taz, town_id, town_name, x, y """
    taz_id = models.CharField('TAZ ID', max_length=10, unique=True)
    town_id = models.IntegerField('Municipality ID')
    town_name = models.CharField(max_length=50)
    x = models.FloatField()
    y = models.FloatField()
    
    
    # GeoDjango-specific: a geometry field and overriding 
    # the default manager with a GeoManager instance.
    geometry = models.MultiPolygonField(srid=26986)
    objects = models.GeoManager()
    
    # So the model is pluralized correctly in the admin.
    class Meta:
        verbose_name_plural = "TAZs"
    
    # Returns the string representation of the model.
    def __unicode__(self):
        return self.taz_id

class StatusChoice(models.Model):
    status = models.CharField(max_length=50, blank=False, null=False)
    
class ZoningChoice(models.Model):
    type = models.CharField(max_length=20, blank=False, null=False)
    description = models.CharField(max_length=255, blank=False, null=False)

class TypeChoice(models.Model):
    type = models.CharField(max_length=50, blank=False, null=False)
    
class Project(models.Model):
    # taz = models.IntegerField('TAZ')
    dd_id = models.IntegerField(primary_key=True)
    name = models.CharField("Project Name (DDname)", max_length=1000)
    description = models.TextField("Project Description ", blank=True, null=True)
    type_id = models.ForeignKey(TypeChoice, blank=True, null=True, help_text="Project Type (DvtType)")
    type_detail = models.TextField("Project Type Detail", blank=True, null=True)
    status_id = models.ForeignKey(StatusChoice, blank=True, null=True, help_text="Project Status (Status)")
    stalled = models.TextField("Project Stalled", blank=True, null=True)
    phase = models.TextField("Project Phase", blank=True, null=True)
    completion = models.IntegerField("Estimated or Actual Year of Completion (ComplYr)", blank=True, null=True)
    area = models.FloatField("Project Area in Acres (PrjAcrs)", blank=True, null=True)
    dev_name = models.TextField("Developer Name", blank=True, null=True)
    website = models.URLField("Project Website (DD_URL)", max_length=1000, blank=True, null=True)
    website_add = models.URLField("Additional Website", max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, editable=False, related_name="project_created_by", blank=True, null=True, help_text="Added By")
    create_date = models.DateTimeField("Create Date", editable=False, auto_now=True)
    last_updated_by = models.ForeignKey(User, related_name="project_last_updated_by", blank=True, null=True, help_text="Last updated by")
    last_modified = models.DateTimeField("Last updated date", editable=False, auto_now=True)
    
    #housing
    total_housing_units = models.IntegerField("Total Housing Units (TotHU)", blank=True, null=True)
    detached_single_fam= models.IntegerField("Detached Single Family (SingFamHU)", blank=True, null=True)
    townhouse_small_multi_fam = models.IntegerField("Townhouse and Small Multifamily (TwnhSmMult)", blank=True, null=True)
    med_large_multi_fam = models.IntegerField("Medium and Large Multifamily (LgMultiFam)", blank=True, null=True)
    age_restricted_pct = models.CharField("Percent Age Restricted (Ovr55)", max_length=20, blank=True, null=True, choices=(("0", "Unknown"), ("YES", "Yes"), ("NO", "No")))
    affordable_pct = models.FloatField("Percent Affordable (PctAffAll)", blank=True, null=True)
    affordable_comment = models.TextField("Affordability Comments", blank=True, null=True)
    group_quarters = models.IntegerField("Group Quarters (GQPOP)", blank=True, null=True)
    
    #total non-res
    nonres_dev = models.IntegerField("Total Nonresidential Development in Square Feet (CommSF)", blank=True, null=True)
    hotel_rooms = models.IntegerField("Hotel rooms (HotelRms)", blank=True, null=True)
    retail_restaurant_pct = models.FloatField("Retail / Restaurant Percent (RetPct)", blank=True, null=True)
    office_medical_pct = models.FloatField("Office / Medical Percent (OfcMdPct)", blank=True, null=True)
    manufacturing_industrial_pct = models.FloatField("Manufacturing / Industrial Percent (IndMfPct)", blank=True, null=True)
    warehouse_trucking_pct = models.FloatField("Warehouse / Trucking Percent (WhsPct)", blank=True, null=True)
    lab_RandD_pct = models.FloatField("Lab / R & D  Percent (RnDPct)", blank=True, null=True)
    edu_institution_pct = models.FloatField("Edu/Institution Percent (EdInstPct)", blank=True, null=True)
    other_pct = models.FloatField("Other (OthPct)", blank=True, null=True)

    #jobs
    jobs = models.IntegerField("Estimated Employment (RptdEmp / EmpLoss)", blank=True, null=True)
    est_emp = models.FloatField("Other jobs per 1000 sqft", blank=True, null=True)
    est_emp_loss = models.IntegerField(blank=True, null=True)
    jobs_per_1000 = models.IntegerField(blank=True, null=True) # jobs per 1000 sq. ft.
    metro_future_discount_pct = models.FloatField("Metro Future Discount (MFDisc)", blank=True, null=True)
    current_trends_discount_pct = models.FloatField("Current trends discount", blank=True, null=True)
    
    #project specific
    parking_spaces = models.IntegerField("Parking Spaces", blank=True, null=True)
    redevelopment = models.CharField("Redevelopment (Rdv)", max_length=20, blank=True, null=True, choices=(("0", "Unknown"), ("YES", "Yes"), ("NO", "No")))
    cluster_subdivision = models.CharField("Cluster Subdivision (ClustOSRD)", max_length=20, blank=True, null=True, choices=(("0", "Unknown"), ("YES", "Yes"), ("NO", "No")))
    zoning_tool_id = models.ForeignKey(ZoningChoice, blank=True, null=True, help_text="Zoning Tool (Ch40)")
    as_of_right = models.TextField("As-of-Right", blank=True, null=True)
    mixed_use = models.CharField("Mixed use project (MxdUse)", max_length=20, blank=True, null=True, choices=(("0", "Unknown"), ("YES", "Yes"), ("NO", "No")))
    total_cost = models.IntegerField("Total project cost", blank=True, null=True)
    total_cost_allocated_pct = models.FloatField("Funding allocated Percent", blank=True, null=True)
    comment = models.TextField("Comments DD_info", blank=True, null=True)
    mapc_comment = models.TextField("MAPC comments", blank=True, null=True)
    
    # GeoDjango-specific: a geometry field and overriding 
    # the default manager with a GeoManager instance.
    location = models.PointField(srid=26986) # SRS mass state plane
    objects = models.GeoManager()
    taz_id = models.ForeignKey(Taz, to_field='taz_id', editable=True, blank=True, null=True)
    
    # find taz for project
    def save(self, *args, **kwargs):
#        # try find taz, otherwise don't validate form! ...probably move to form_save
        # l = 'POINT (243617.8433000145596452 901646.1310999535489827)'
#        t = Taz.objects.get(geometry__contains=l)
#        self.taz = t
         # dummy until we figure another solution out
        # if not self.id:
        try:
            self.taz = Taz.objects.get(geometry__contains=self.location)
        except:
            self.taz = None
            # geometry__contains=self.location
        #    self.last_modified = datetime.date.today()
        # self.comments = self.location
        
        self.last_modified = datetime.datetime.today()
        # return super(Entry, self).save()
        super(Project, self).save(*args, **kwargs)
        
# topology rule
#    def clean(self): 
#        tv = Taz.objects.filter(geometry__contains=self.location)
#        if len(tv) <= 1:
#            raise ValidationError(len('Location is not within a TAZ. Please re-locate project.'))
           
    # So the model is pluralized correctly in the admin.
    class Meta:
        verbose_name_plural = "Projects"

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name
    
    def town_name(self):
        return self.taz.town_name

#    the short elegant version
#    def get_fields(self):
#        return [(field.name, field.value_to_string(self)) for field in Project._meta.fields]

#   more control over fields 
    def get_all_fields(self):
        """Returns a list of all field names on the instance."""
        """http://stackoverflow.com/questions/2170228/django-iterate-over-model-instance-field-names-and-values-in-template/2226150#2226150"""
        fields = []
        for f in self._meta.fields:
    
            fname = f.name        
            # resolve picklists/choices, with get_xyz_display() function
            get_choice = 'get_'+fname+'_display'
            if hasattr( self, get_choice):
                value = getattr( self, get_choice)()
            else:
                try :
                    value = getattr(self, fname)
                except User.DoesNotExist:
                    value = None
    
            # only display fields with values and skip some fields entirely
            if f.editable and value and f.name not in ('id', 'name', 'location', 'confirmed_by', 'located_by', 'located', 'confirmed') :
    
                fields.append(
                  {
                   'label':f.verbose_name, 
                   'name':f.name, 
                   'value':value,
                  }
                )
        return fields


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # fields = ['name', 'status', 'comments', 'location']
        exclude = ['taz', 'removed']
        widgets = {
           'comments': Textarea(attrs={'cols': 80, 'rows': 20}),
           'location': HiddenInput(),
           'confirmed_by': HiddenInput(), 
           'located_by': HiddenInput(),
        }
