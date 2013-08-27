from django.db import models
from django.utils.translation import ugettext as _
from development.models import Project

class ModeratedProject(Project):
    """
    Project awaiting moderation. Registered Users not belonging to
    any group have their edits created using a ModeratedProject as
    opposed to a Project. Once approved by a Municipal User / Admin,
    the ModeratedProject updates the corresponding Project.
    """
    project    = models.ForeignKey(Project, null=True, related_name='real_project')
    approved   = models.BooleanField(default=False)
    completed  = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('ModeratedProject')
        verbose_name_plural = _('ModeratedProjects')
        ordering = ['project',]

    def __unicode__(self):
        return str(self.project)