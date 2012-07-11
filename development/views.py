from django.shortcuts import render_to_response
from django.template import RequestContext

from development.models import Project
from development.forms import ProjectfilterForm, ProjectForm

def search(request):
    projectfilterform = ProjectfilterForm()
    return render_to_response('development/search.html', locals(), context_instance=RequestContext(request))


def detail(request, dd_id):
    try:
        project = Project.objects.transform(4326).get(pk=dd_id)
    except MyModel.DoesNotExist:
        raise Http404

    return render_to_response('development/detail.html', locals(), context_instance=RequestContext(request))


def add(request):

    project = ProjectForm()

    return render_to_response('development/edit.html', locals(), context_instance=RequestContext(request))