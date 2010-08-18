from django import forms
from registration.forms import RegistrationForm
from django.utils.translation import ugettext_lazy as _
from communitycomments.accounts.models import UserProfile
from registration.models import RegistrationProfile
from django.contrib.auth.models import User

from communitycomments.projects.models import Taz, Town

attrs_dict = { 'class': 'required' }

class ExtendedRegistrationForm(RegistrationForm):
    first_name = forms.CharField(label='First name', max_length=30, widget=forms.TextInput())
    last_name = forms.CharField(label='Last name', max_length=30, widget=forms.TextInput())
    town = forms.ModelChoiceField(label='Municipality', queryset=Town.objects.filter(geometry__bboverlaps=Taz.objects.all().collect()).order_by('town_name'), empty_label='No Municipality selected')
    position = forms.CharField(label='Position in Municipality', max_length=100, widget=forms.TextInput(attrs=attrs_dict))
    
    # filter(geometry__bboverlaps=Taz.objects.all().collect())
    # all()
    # town = forms.CharField(label='Municipality', max_length=50, widget=forms.TextInput(attrs=attrs_dict))
    # t = Taz.objects.all().values('town_name').annotate(count=Count('town_name')).order_by('town_name')
    # forms.ModelChoiceField(queryset=Taz.objects.all().values('town_name').annotate(count=Count('town_name')).order_by('town_name'), empty_label="(Nothing)")
    
    def save(self, profile_callback=None):
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
        password=self.cleaned_data['password1'],
        email=self.cleaned_data['email'])
        
        # django-registration doesn't include first and last name when adding a new User object
        try:
            django_user = User.objects.get(username=new_user.username)
            django_user.first_name = self.cleaned_data['first_name']
            django_user.last_name = self.cleaned_data['last_name']
            django_user.save()
        except User.DoesNotExist:
            pass
        
        new_profile = UserProfile(user=new_user, town=self.cleaned_data['town'], position=self.cleaned_data['position'])
        new_profile.save()
        return new_user