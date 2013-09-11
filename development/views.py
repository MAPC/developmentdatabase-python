from django.shortcuts import render_to_response, redirect
from django.core.mail import send_mail
from django.template  import RequestContext, Context
from django.template.loader import get_template
from django.http      import Http404, HttpResponse
from django.contrib                 import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.gis.geos        import GEOSGeometry
from django.core.exceptions         import FieldError


import json
import csv

from development.models import Project, User
from tim.models import ModeratedProject
from development.forms import ProjectfilterForm, ProjectForm, ModeratedProjectForm

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

    if request.user.is_authenticated():
        logged_in = True
    else:
        logged_in = False

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
        projects = Project.display.transform(4326).filter(**kwargs)
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

    projects = Project.display.transform(4326).filter(**kwargs)

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
# @user_passes_test(lambda u: u.groups.filter(name='Project Editors').count() > 0, login_url='/')
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
def update(request, dd_id):
    """ Update existing project """

    try:
        project = Project.objects.transform(4326).get(pk=dd_id)
    except Project.DoesNotExist:
        raise Http404

    # TODO: refactor this whole block

    if has_permissions(request.user, project.taz.municipality):     

        user = request.user.profile

        if request.method == 'POST':
            mod_proj = ModeratedProject.new_from_project(project)
            mod_proj.user = request.user

            updated_project = ModeratedProjectForm(request.POST, instance=mod_proj)
            
            if updated_project.is_valid():
                entry = updated_project.save(commit=False)
                new_location = GEOSGeometry(entry.location)
                new_location.srid = 4326
                new_location.transform(26986)

                entry.location = new_location

                entry.save(user=request.user, update_walkscore=True)

                if user.is_trusted() or user.is_municipal():
                    # TODO: refactor
                    entry.accept()
                    municipal_users = User.objects.filter(profile__municipality=entry.municipality())
                    emails = [ user.email for user in municipal_users ]
                    
                    body = get_template('mail_templates/new_pending_edit.html').render(
                        Context({
                            'project_id' : entry.project.dd_id,
                            'project_name' : entry.project.ddname,
                            'municipality_name' : entry.municipality().name,
                            'project': entry
                       })
                    )

                    send_mail(
                        'Development Database: New Edit',
                        body,
                        emails.pop(),
                        emails,
                        fail_silently=False)
                    
                    messages.add_message(request, messages.INFO, 'You are a trusted user, so your edits will be published immediately.')
                else:
                    # TODO: refactor
                    municipal_users = User.objects.filter(profile__municipality=entry.municipality())
                    emails = [ user.email for user in municipal_users ]
                    
                    body = get_template('mail_templates/new_pending_edit.html').render(
                        Context({
                            'project_id' : entry.project.dd_id,
                            'project_name' : entry.project.ddname,
                            'municipality_name' : entry.municipality().name,
                            'project': entry
                       })
                    )

                    send_mail(
                        'Development Database: New Edit',
                        body,
                        emails.pop(),
                        emails,
                        fail_silently=False)

                    messages.add_message(request, messages.INFO, 'Your edits will be moderated.')
                    
                messages.add_message(request, messages.INFO, 'Your edits to %s were saved.' % (entry.ddname) )
                return redirect('detail', dd_id=entry.project.dd_id)
            else:
                messages.add_message(request, messages.INFO, "There were errors in your submission: %s" % (updated_project.errors))
                return redirect('update', dd_id=project.dd_id)

        else:
            project = ModeratedProjectForm(instance=ModeratedProject.new_from_project(project))

    else:
        messages.add_message(request, messages.INFO, 'You are not authorized to edit projects outside your municipality.' )
        return redirect('detail', dd_id=dd_id)

    return render_to_response('development/update.html', locals(), context_instance=RequestContext(request))


