from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail

from development.models import Municipality

from userena.models import UserenaBaseProfile
from userena.signals import signup_complete

class Profile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile')
    municipality = models.ForeignKey(Municipality, null=True, help_text='The municipality you would like to add and edit projects.')
    position = models.CharField(max_length=100, null=True, help_text='Your postion in that municipality.')

    def is_municipal(self):
        if self.user.groups.filter(name="Municipal Users").count() > 0:
            return True
        return False

    def is_trusted(self):
        if self.user.groups.filter(name="Trusted Users").count() > 0:
            return True
        return False    


@receiver(signup_complete)
def my_callback(sender, **kwargs):
    user = kwargs.pop('user', None)
    subject = 'New user %s signed up for Development Database.' % (user)
    body = 'Verify if user can be added to Project Editor group at http://dd.mapc.org/admin/'
    send_mail(subject, body, 'webapp@mapc.org', ['cspanring@mapc.org'], fail_silently=False)