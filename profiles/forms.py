from django import forms
from django.utils.translation import ugettext_lazy as _

from userena.forms import SignupForm

from development.models import Municipality

class SignupFormExtra(SignupForm):
    """ 
    Adding extra fields to the signup form
    """
    first_name = forms.CharField(label=_(u'First name'),
                                 max_length=30,
                                 required=False)

    last_name = forms.CharField(label=_(u'Last name'),
                                max_length=30,
                                required=False)

    municipality =forms.ModelChoiceField(label=_(u'Your Municipality'), queryset=Municipality.objects.all())

    position = forms.CharField(label=_(u'Your Position'), max_length=100, required=True)

    def __init__(self, *args, **kw):
        """
        A bit of hackery to change the field order.
        """
        super(SignupFormExtra, self).__init__(*args, **kw)
        # Put the first and last name at the top
        new_order = self.fields.keyOrder[:-4]
        new_order.insert(1, 'municipality')
        new_order.insert(2, 'position')
        new_order.insert(4, 'first_name')
        new_order.insert(5, 'last_name')
        self.fields.keyOrder = new_order

    def save(self):
        """ 
        Override the save method to save the user and profile
        """
        new_user = super(SignupFormExtra, self).save()

        new_user_profile = new_user.get_profile()
        new_user_profile.position = self.cleaned_data['position']
        new_user_profile.municipality = self.cleaned_data['municipality']
        new_user_profile.save()

        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user
