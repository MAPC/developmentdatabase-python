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
    municipality = models.ForeignKey(Municipality)
    position = models.CharField(max_length=100)