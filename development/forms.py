from django import forms

from bootstrap.forms import BootstrapForm, BootstrapMixin, Fieldset

from development.models import Project, Municipality


class ProjectfilterForm(BootstrapMixin, forms.ModelForm):
    """
    Form used to query projects with Tastypie
    """

    municipality = forms.ModelChoiceField(queryset=Municipality.objects.filter(taz__project__isnull=False).order_by('muni_id').distinct('muni_id'))

    class Meta:
        model = Project
        fields = ('municipality', 'ddname', 'projecttype', 'status', 'complyr', 'tothu', 'ovr55', 'pctaffall', 'totemp', )
        help_tooltip = True


class ProjectForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = Project
        widgets = {
            'location': forms.HiddenInput(),
        }