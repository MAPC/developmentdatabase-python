from django.db import models
from django.contrib.gis.db import models

# Create your models here.

class Project(models.Model):
    taz = models.IntegerField('TAZ')
    name = models.CharField(max_length=200)
    status_choices = (
                      ('completed', 'Completed'),
                      ('construction', 'Under construction'),
                      ('planning', 'Advanced planning/permitting'),
                      )
    status = models.CharField(max_length=20, blank=True, choices=status_choices)
    compl_date = models.DateField('Estimated date of completion', blank=True, null=True)
    area = models.FloatField('Project area [acres]', blank=True, null=True)
    redevelopment = models.BooleanField('Redevelopment of developed land?')
    hd_singlefam_units = models.IntegerField('Single family homes', blank=True, null=True)
    hd_attached_units = models.IntegerField('Attached single family homes', blank=True, null=True)
    hd_apt_units = models.IntegerField('Apartments and condos', blank=True, null=True)
    hd_cluster = models.BooleanField('Cluster subdivision?')
    hd_over55 = models.BooleanField('Over 55?')
    hd_mixeduse = models.BooleanField('Mixed use project?')
    hd_40b = models.BooleanField('40B? 40R?')
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

    # So the model is pluralized correctly in the admin.
    class Meta:
        verbose_name_plural = "Projects"

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name
    