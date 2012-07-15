from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from development.models import Municipality

from userena.models import UserenaBaseProfile

class Profile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile')
    municipality = models.ForeignKey(Municipality, null=True, help_text='The municipality you would like to add and edit projects.')
    position = models.CharField(max_length=100, null=True, help_text='Your postion in that municipality.')