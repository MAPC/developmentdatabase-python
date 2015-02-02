from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save
from development.models import Project
from django.contrib.auth.models import User
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
    project    = models.ForeignKey(Project, related_name='moderated_project')
    user       = models.ForeignKey(User, null=True)
    
    class Meta:
        verbose_name        = _('ModeratedProject')
        verbose_name_plural = _('ModeratedProjects')

    # def __unicode__(self):
        # return str(self.project.ddname) or 'Untitled'

    def diff(self):
        moderated_project = self
        project           = self.project

        diff = {}

        frozen_fields   = [ 'last_modified', 'created', 'dd_id', 'moderated_project', 'location' ]
        editable_fields = list( set(moderated_project._meta.fields).intersection(project._meta.fields) )

        for field in editable_fields:
            if field.name in frozen_fields: continue
            proposed = getattr(moderated_project, field.name, None)
            current  = getattr(project,           field.name, None)

            if proposed != current:
                diff[field.verbose_name] = {'name': field.verbose_name.title(), 'current': current, 'proposed': proposed}

        return diff


    def changed_fields(self):
        moderated_project = self
        project           = self.project_object

        fields = list()

        for field in set( moderated_project._meta.fields + project._meta.fields ):
            proposed = getattr(moderated_project, field.name, None)
            current  = getattr(project,           field.name, None)

            if proposed != current:
                fields.append(field.name)

        return fields


    def accept(self):
        self.accepted  = True
        self.completed = True
        self.update_project_with_edits()
        self.save()

    
    def decline(self):
        self.accepted  = False
        self.completed = True
        self.save()

    def reopen(self):
        self.accepted  = False
        self.completed = False
        self.save()

    def update_project_with_edits(self):
        project = self.project
        for edit, value in self.diff().iteritems():
            project.__setattr__(edit, value['proposed'])
        project.save()

    @classmethod
    def new_from_project(self, project):
        """
        Creates a new instance of ModeratedProject based on an
        existing Project object.
        """
        moderated_project_fields = set( self._meta.get_all_field_names() )
        project_fields           = set( project._meta.get_all_field_names() )

        common_fields = project_fields.intersection(moderated_project_fields)
        common_fields.remove('dd_id') # moderated_project.dd_id = None
        common_fields.remove('moderated_project')

        moderated_project = ModeratedProject(project=project)

        for field in common_fields:
            moderated_project.__setattr__(field, getattr(project, field))
        
        # moderated_project.save()
        return moderated_project


# Signals

# TODO: 
# Notify Municipal User of a new Moderated Project.
# post_save.connect(notify_municipal_user, sender=ModeratedProject)

# Notify User of their changes being accepted or declined
# post_save.connect(notify_registered_user, )
# will need: moderated_project.[accepted, completed, user]



