from django.shortcuts import render_to_response, redirect
from django.template  import RequestContext
from django.http      import Http404, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.gis.geos        import GEOSGeometry
from django.core.exceptions         import FieldError

import json
import csv

from development.models import Project
from development.forms import ProjectfilterForm, ProjectForm

def has_permissions(user, municipality):
    if not user.is_anonymous() and (user.groups.filter(name='MAPC Staff').count() > 0 or user.get_profile().municipality == municipality):
        return True
    return False

def search(request):
    """ Filter projects """

    projectfilterform = ProjectfilterForm()

    return render_to_response('development/search.html', locals(), context_instance=RequestContext(request))


def detail(request, dd_id):
    """ Show project details """

    try:
        project = Project.objects.transform(4326).get(pk=dd_id)
        permissions = has_permissions(request.user, project.taz.municipality)
    except Project.DoesNotExist:
        raise Http404

    return render_to_response('development/detail.html', locals(), context_instance=RequestContext(request))


def projects_geojson(request):
    """ 
        Return GeoJSON represantion of filtered projects.
    """

    querydict = request.GET
    kwargs = querydict.dict()
    features = []

    format = querydict.get('format', None)

    # GeoJSON default
    try:
        projects = Project.for_display.transform(4326).filter(**kwargs)
        for project in projects:
            geojson_prop = dict(
                ddname = project.ddname.title(), 
                url = project.get_absolute_url(),
            )
            geojson_geom = json.loads(project.location.geojson)
            geojson_feat = dict(type='Feature', geometry=geojson_geom, properties=geojson_prop)
            features.append(geojson_feat)
        response = dict( type='FeatureCollection', features=features )
    except FieldError:
        response = dict( type='FeatureCollection', features=features )

    return HttpResponse(json.dumps(response), mimetype='application/json')


@login_required
def projects_csv(request):
    """
        Return filtered projects as CSV for download.
    """

    querydict = request.GET
    kwargs = querydict.dict()
    features = []

    format = querydict.get('format', None)

    projects = Project.for_display.transform(4326).filter(**kwargs)

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=projects.csv'
    writer = csv.writer(response)

    field_names = ['dd_id', 'ddname', 'status', 'prjacrs', 'tothu', 'commsf'] 
    # Write a first row with header information
    writer.writerow(['Project ID', 'Name', 'Status', 'Project Area', 'Total Housing Units', 'Total Non-Residential Development'])

    # Write data rows
    for project in projects:
        try:
            writer.writerow([getattr(project, field) for field in field_names])
        except UnicodeEncodeError:
            print 'Could not export data row.'

    return response


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Project Editors').count() > 0, login_url='/')
def add(request):
    """ Add new project """

    # save form
    if request.method == 'POST':
        new_project = Project()
        project = ProjectForm(request.POST, instance=new_project)
        # TODO: mixin permission check
        if project.is_valid():
            # transform location
            entry = project.save(commit=False)
            new_location = GEOSGeometry(entry.location)
            new_location.srid = 4326
            new_location.transform(26986)
            entry.location = new_location
            entry.save( user=request.user, update_walkscore=True )
            return redirect('detail', dd_id=entry.dd_id)
    # show empty form
    else:
        project = ProjectForm()

    return render_to_response('development/update.html', locals(), context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Project Editors').count() > 0, login_url='/')
def update(request, dd_id):
    """ Update existing project """

    try:
        project = Project.objects.transform(4326).get(pk=dd_id)
    except Project.DoesNotExist:
        raise Http404

    if has_permissions(request.user, project.taz.municipality):     
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
                entry.save( user=request.user, update_walkscore=True )
                return redirect('detail', dd_id=entry.dd_id)
        # show projectform
        else:
            project = ProjectForm(instance=project)
    else:
        # TODO: better usability, show user a message what happened
        return redirect('detail', dd_id=dd_id)

    return render_to_response('development/update.html', locals(), context_instance=RequestContext(request))


