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
    taz = models.ForeignKey(Taz, blank=True, null=True)
    name = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    type_id = models.ForeignKey(TypeChoice, blank=True, null=True)
    type_detail = models.TextField(blank=True, null=True)
    status_id = models.ForeignKey(StatusChoice, blank=True, null=True)
    stalled = models.TextField("Project Stalled?", blank=True, null=True)
    phase = models.TextField(blank=True, null=True)
    completion = models.IntegerField(blank=True, null=True)
    area = models.FloatField('Project area [acres]', blank=True, null=True)
    dev_name = models.TextField(blank=True, null=True)
    website = models.URLField(max_length=1000, blank=True, null=True)
    website_add = models.URLField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, editable=False, related_name="project_created_by", blank=True, null=True)
    create_date = models.DateTimeField(editable=False, auto_now=True)
    last_updated_by = models.ForeignKey(User, related_name="project_last_updated_by", blank=True, null=True)
    last_modified = models.DateTimeField(editable=False, auto_now=True)
    
    #housing
    total_housing_units = models.IntegerField(blank=True, null=True)
    detached_single_fam= models.IntegerField(blank=True, null=True)
    townhouse_small_multi_fam = models.IntegerField(blank=True, null=True)
    med_large_multi_fam = models.IntegerField(blank=True, null=True)
    age_restricted_pct = models.FloatField(blank=True, null=True)
    affordable_pct = models.FloatField(blank=True, null=True)
    affordable_comment = models.TextField(blank=True, null=True)
    group_quarters = models.IntegerField(blank=True, null=True)
    nonres_dev = models.IntegerField(blank=True, null=True)
    hotel_rooms = models.IntegerField(blank=True, null=True)
    retail_restaurant_pct = models.FloatField(blank=True, null=True)
    office_medical_pct = models.FloatField(blank=True, null=True)
    manufacturing_industrial_pct = models.FloatField(blank=True, null=True)
    warehouse_trucking_pct = models.FloatField(blank=True, null=True)
    lab_RandD_pct = models.FloatField(blank=True, null=True)
    edu_institution_pct = models.FloatField(blank=True, null=True)
    other_pct = models.FloatField(blank=True, null=True)
    
    #jobs
    jobs = models.IntegerField(blank=True, null=True)
    est_emp = models.FloatField(blank=True, null=True)
    est_emp_loss = models.IntegerField(blank=True, null=True)
    jobs_per_1000 = models.IntegerField(blank=True, null=True) # jobs per 1000 sq. ft.
    metero_future_discount_pct = models.FloatField(blank=True, null=True)
    current_trends_discount_pct = models.FloatField(blank=True, null=True)
    
    #project specific
    parking_spaces = models.IntegerField(blank=True, null=True)
    redevelopment = models.CharField('Redevelopment of developed land?', max_length=50, blank=True, null=True) # FIXME: make choice options
    cluster_subdivision = models.FloatField(blank=True, null=True)
    zoning_tool_id = models.ForeignKey(ZoningChoice, blank=True, null=True)
    as_of_right = models.TextField(blank=True, null=True)
    mixed_use = models.FloatField(blank=True, null=True)
    total_cost = models.IntegerField(blank=True, null=True)
    total_cost_allocated_pct = models.FloatField(blank=True, null=True)
    comment = models.TextField('Comment', blank=True, null=True)
    mapc_comment = models.TextField('Comment', blank=True, null=True)
    
    # GeoDjango-specific: a geometry field and overriding 
    # the default manager with a GeoManager instance.
    location = models.PointField(srid=26986) # SRS mass state plane
    objects = models.GeoManager()
    
    # find taz for project
    def save(self, *args, **kwargs):
        try:
            # find TAZ for project location
            self.taz = Taz.objects.get(geometry__contains=self.location)
        except:
            self.taz = None
        
        self.last_modified = datetime.datetime.today()
        
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