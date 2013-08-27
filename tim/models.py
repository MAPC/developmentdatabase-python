from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from development.models import Project

class ModeratedProject(Project):
    """
    Project awaiting moderation. Registered Users not belonging to
    any group have their edits created using a ModeratedProject as
    opposed to a Project. Once approved by a Municipal User / Admin,
    the ModeratedProject updates the corresponding Project.
    """
    approved   = models.BooleanField(default=False)
    completed  = models.BooleanField(default=False)

    content_type   = models.ForeignKey(ContentType) 
    object_id      = models.PositiveIntegerField()
    project_object = generic.GenericForeignKey('content_type', 'object_id')

    # Project, null=True, related_name='real_project'

    
    class Meta:
        verbose_name        = _('ModeratedProject')
        verbose_name_plural = _('ModeratedProjects')
        ordering            = ['object_id',]

    def __unicode__(self):
        return str(self.project_object)