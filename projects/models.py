from django.contrib.gis.db import models
# from django import forms
from django.forms import ModelForm, Textarea

# Create your models here.

class Project(models.Model):
    # taz = models.IntegerField('TAZ')
    taz = models.ForeignKey('projects.Taz', editable=False)
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
    comments = models.TextField('Comments', blank=True)
    last_modified = models.DateTimeField(editable=False, auto_now=True)
    confirmed = models.BooleanField()
    confirmed_by = models.CharField(max_length=30, blank=True)
    located = models.BooleanField()
    located_by = models.CharField(max_length=30, blank=True)
    
    # GeoDjango-specific: a geometry field and overriding 
    # the default manager with a GeoManager instance.
    location = models.PointField(srid=26986) # SRS mass state plane
    objects = models.GeoManager()

    # find taz for project
#    def save(self, *args, **kwargs):
#        try find taz, otherwise don't validate form! ...probably move to form_save
#        self.taz = Taz.objects.filter(geometry__contains=self.location)[0].taz_id
#        super(Project, self).save(*args, **kwargs)
        
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
        fields = ('name', 'status', 'comments')
        widgets = {
           'comments': Textarea(attrs={'cols': 80, 'rows': 20}),
        }

"""
class ProjectForm(forms.Form):
    name = forms.CharField(max_length=200)
"""
   
class Taz(models.Model):
    """ taz, town_id, town_name, x, y """
    taz_id = models.CharField('TAZ ID', max_length=10, primary_key=True)
    town_id = models.IntegerField('Town ID')
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
    