from django.db import models
from django.contrib.gis.db import models

# Create your models here.

class Project(models.Model):
    taz = models.IntegerField()
    name = models.CharField(max_length=200)
    status_choices = (
                      ('completed', 'Completed'),
                      ('construction', 'Under construction'),
                      ('planning', 'Advanced planning/permitting'),
                      )
    status = models.CharField(max_length=20, choices=status_choices)
    area = models.FloatField()
    redevelopment = models.BooleanField()
    hd_singlefam_units = models.IntegerField()
    hd_attached_units = models.IntegerField()
    hd_apt_units = models.IntegerField()
    hd_cluster = models.BooleanField()
    hd_over55 = models.BooleanField()
    hd_mixeduse = models.BooleanField()
    hd_40b = models.BooleanField()
    ed_jobs = models.IntegerField()
    ed_sqft = models.FloatField()
    ed_type = models.CharField(max_length=200)
    comments = models.TextField()
    edit_date = models.DateTimeField('date edited')
    confirmed = models.BooleanField()
    located = models.BooleanField()
    user = models.CharField(max_length=50)
    
    # GeoDjango-specific: a geometry field and overriding 
    # the default manager with a GeoManager instance.
    location = models.PointField() # SRS mass state plane
    objects = models.GeoManager()

    # So the model is pluralized correctly in the admin.
    class Meta:
        verbose_name_plural = "Projects"

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name
    