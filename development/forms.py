from django import forms

from bootstrap.forms import BootstrapForm, BootstrapMixin, Fieldset

from development.models import Project, Municipality
from tim.models import ModeratedProject


class ProjectfilterForm(BootstrapMixin, forms.ModelForm):
    """
    Form used to query projects with Tastypie
    """

    municipality = forms.ModelChoiceField(queryset=Municipality.objects.filter(taz__project__isnull=False).order_by('muni_id').distinct('muni_id'))

    class Meta:
        model = Project
        fields = (
            'municipality', 'ddname', 'projecttype', 'status', 'complyr', 'prjacrs', 'rdv', 'stalled', 'phased',
            'tothu', 'singfamhu', 'twnhsmmult', 'lgmultifam', 'gqpop', 'ovr55', 'pctaffall', 'clustosrd', 'ch40', 
            'totemp', 'commsf', 'retpct', 'ofcmdpct', 'indmfpct', 'whspct', 'rndpct', 'othpct', 'hotelrms',
            'parking_spaces', 'as_of_right', 'todstation', 'total_cost',
            )
        help_tooltip = True


class ProjectForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = Project
        widgets = {
            'location': forms.HiddenInput(),
        }

class ModeratedProjectForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = ModeratedProject
        exclude = ('user', 'project', 'est_employment', )
        widgets = {
            'location': forms.HiddenInput(),
        }