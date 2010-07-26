from django.contrib.gis.db import models
# from django import forms
from django.forms import ModelForm, Textarea, HiddenInput

import datetime
from django.core.exceptions import ValidationError
# required for finding taz for project location
# from django.contrib.gis.geos import *

from django.template import RequestContext

# Create your models here.

class Project(models.Model):
    # taz = models.IntegerField('TAZ')
    taz = models.ForeignKey('projects.Taz', to_field='taz_id', editable=False)
    name = models.CharField(max_length=200)
    status_choices = (
                      ('completed', 'Completed'),
                      ('construction', 'Under construction'),
                      ('planning', 'Advanced planning/permitting'),
                      )
    status = models.CharField(max_length=20, blank=True, null=True, choices=status_choices)
    compl_date = models.DateField('Estimated date of completion', blank=True, null=True)
    area = models.FloatField('Project area [acres]', blank=True, null=True)
    redevelopment = models.BooleanField('Redevelopment of developed land?')
    hd_singlefam_units = models.IntegerField('Single family homes', blank=True, null=True)
    hd_attached_units = models.IntegerField('Attached single family homes', blank=True, null=True)
    hd_apt_units = models.IntegerField('Apartments and condos', blank=True, null=True)
    hd_cluster = models.BooleanField('Cluster subdivision?')
    hd_over55 = models.BooleanField('Over 55?')
    hd_mixeduse = models.BooleanField('Mixed use project?')
    zoning_tools = (
                    ('40B', 'Chapter 40B Comprehensive Permit Law'),
                    ('40R', 'Chapter 40R Smart Growth Zoning and Housing Production Law')
                    )
    zoning_tool = models.CharField(max_length=10, blank=True, null=True, choices=zoning_tools)
    ed_jobs = models.IntegerField('Jobs or Job losses', blank=True, null=True)
    ed_sqft = models.FloatField('Square footage', blank=True, null=True)
    ed_type = models.CharField('Type of development', max_length=200, blank=True)
    comments = models.TextField('Comments', blank=True, null=True)
    last_modified = models.DateTimeField(editable=False, auto_now=True)
    confirmed = models.BooleanField()
    confirmed_by = models.CharField(max_length=30, blank=True)
    located = models.BooleanField()
    located_by = models.CharField(max_length=30, blank=True)
    
    # user = models.ForeignKey(User, editable=False)
    
    # GeoDjango-specific: a geometry field and overriding 
    # the default manager with a GeoManager instance.
    location = models.PointField(srid=26986) # SRS mass state plane
    objects = models.GeoManager()

    # find taz for project
    def save(self, *args, **kwargs):
#        # try find taz, otherwise don't validate form! ...probably move to form_save
        # l = 'POINT (243617.8433000145596452 901646.1310999535489827)'
#        t = Taz.objects.get(geometry__contains=l)
#        self.taz = t
         # dummy until we figure another solution out
        # if not self.id:
        # try
        self.taz = Taz.objects.get(geometry__contains=self.location)
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


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'status', 'comments', 'location']
        exclude = ['taz']
        widgets = {
           'comments': Textarea(attrs={'cols': 80, 'rows': 20}),
           'location': HiddenInput(),
        }
    


"""
class ProjectForm(forms.Form):
    name = forms.CharField(max_length=200)
"""
   
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
    
class Town(models.Model):
    town_id = models.IntegerField('Municipality ID')
    town_name = models.CharField('Municipality Name', max_length=50)
    type = models.CharField(max_length=10)
    
    # GeoDjango-specific: a geometry field and overriding 
    # the default manager with a GeoManager instance.
    geometry = models.MultiPolygonField(srid=26986)
    objects = models.GeoManager()
    
    # So the model is pluralized correctly in the admin.
    class Meta:
        verbose_name_plural = "Towns"
    
    # Returns the string representation of the model.
    def __unicode__(self):
        return self.town_name
    