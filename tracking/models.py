from django.db import models
import datetime

from communitycomments.projects.models import Town
from communitycomments.accounts.models import UserProfile
from django.contrib.auth.models import User
# Create your models here.

class Note(models.Model):
    town = models.ForeignKey('projects.Town')
    desc = models.TextField('Text')
    type_choices = (
                    ('email', 'Email'),
                    ('note', 'Note'),
                    ('todo', 'ToDo'),
                    )
    type = models.CharField(max_length=10, blank=True, null=True, choices=type_choices)
    action = models.BooleanField('Requires action')
    attachment = models.FileField(upload_to='attachments', max_length=100, blank=True, null=True)
    # modified_by = models.ForeignKey(User)
    contact = models.ForeignKey(UserProfile, blank=True, null=True)
    last_modified = models.DateTimeField(editable=False, auto_now=True)
        
    def town_name(self):
        return self.town.town_name
    
    def excerpt(self):
        return self.desc[:100]
    
    def attachment_name(self):
        if self.attachment:
            return self.attachment.name[12:]
        else:
            return '-'
    
    def save(self, *args, **kwargs):
        self.last_modified = datetime.datetime.today()
        super(Note, self).save(*args, **kwargs)