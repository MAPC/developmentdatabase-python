from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save
from development.models import Project
from .signals import notify_municipal_user

class ModeratedProject(Project):
    """
    Project awaiting moderation. Registered Users not belonging to
    any group have their edits created using a ModeratedProject as
    opposed to a Project. Once approved by a Municipal User / Admin,
    the ModeratedProject updates the corresponding Project.
    """
    accepted   = models.BooleanField(default=False)
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


    @classmethod
    def new_from_project(self, project):
        """
        Creates a new instance of ModeratedProject based on an
        existing Project object.
        """
        project_fields = project._meta.get_all_field_names()
        modproj_fields = self._meta.get_all_field_names()
        common_fields  = list( set(project_fields).intersection(modproj_fields) )

        moderated_project = ModeratedProject(project_object=project)

        for field in common_fields:
            moderated_project.__setattr__(field, getattr(project, field))

    def changes(self):
        pass


# post_save.connect(notify_municipal_user, sender=ModeratedProject)



