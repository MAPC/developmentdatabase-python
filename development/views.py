from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import GEOSGeometry

from development.models import Project
from development.forms import ProjectfilterForm, ProjectForm

def search(request):
    """ Filter projects """

    projectfilterform = ProjectfilterForm()

    return render_to_response('development/search.html', locals(), context_instance=RequestContext(request))


def detail(request, dd_id):
    """ Show project details """

    try:
        project = Project.objects.transform(4326).get(pk=dd_id)
    except Project.DoesNotExist:
        raise Http404

    return render_to_response('development/detail.html', locals(), context_instance=RequestContext(request))


@login_required
def add(request):
    """ Add new project """

    # save form
    if request.method == 'POST':
        new_project = Project()
        project = ProjectForm(request.POST, instance=new_project)
        if project.is_valid():
            # transform location
            entry = project.save(commit=False)
            new_location = GEOSGeometry(entry.location)
            new_location.srid = 4326
            new_location.transform(26986)
            entry.location = new_location
            entry.save()
            return redirect('detail', dd_id=entry.dd_id)
    # show empty form
    else:
        project = ProjectForm()

    return render_to_response('development/update.html', locals(), context_instance=RequestContext(request))


@login_required
def update(request, dd_id):
    """ Update existing project """

    try:
        project = Project.objects.transform(4326).get(pk=dd_id)
    except Project.DoesNotExist:
        raise Http404

    # update project
    if request.method == 'POST':
        updated_project = ProjectForm(request.POST, instance=project)
        if updated_project.is_valid():
            # transform location
            entry = updated_project.save(commit=False)
            new_location = GEOSGeometry(entry.location)
            new_location.srid = 4326
            new_location.transform(26986)
            entry.location = new_location
            entry.save()
            return redirect('detail', dd_id=entry.dd_id)
    # show projectform
    else:
        project = ProjectForm(instance=project)

    return render_to_response('development/update.html', locals(), context_instance=RequestContext(request))


