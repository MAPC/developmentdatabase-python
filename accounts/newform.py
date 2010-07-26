from django import forms
from registration.forms import RegistrationForm
from django.utils.translation import ugettext_lazy as _
from accounts.models import UserProfile
from registration.models import RegistrationProfile

from projects.models import Taz, Town

attrs_dict = { 'class': 'required' }

class ExtendedRegistrationForm(RegistrationForm):
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
        new_profile = UserProfile(user=new_user, town=self.cleaned_data['town'], position=self.cleaned_data['position'])
        new_profile.save()
        return new_user