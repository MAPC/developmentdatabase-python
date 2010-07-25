from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm
from communitycomments.projects.models import Project, ProjectForm, Taz

from django.template import RequestContext

# required for finding taz for project location
from django.contrib.gis.geos import GEOSGeometry

def index(request):
    project_list = Project.objects.transform(900913).all().order_by('-last_modified')[:25]
    
    # stations = GreenlineStation.objects.transform(900913).all()
    
    return render_to_response('projects/index.html', 
                              {'project_list': project_list}, 
                              context_instance=RequestContext(request))

def community(request, community_name):
    project_list = Project.objects.transform(900913).filter(taz__town_name__iexact=community_name)[:25]
    return render_to_response('projects/community.html', 
                              {'project_list': project_list}, 
                              context_instance=RequestContext(request))

def detail(request, project_id):
    p = get_object_or_404(Project, pk=project_id)
    return render_to_response('projects/detail.html', 
                              {'project': p}, 
                              context_instance=RequestContext(request))
    
def geojson(request, project_id):
     project = Project.objects.transform(4326).get(pk = project_id)     
     return render_to_response('projects/project.geojson', 
                              {'project': project}, 
                              context_instance=RequestContext(request))

def add(request):
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			entry = form.save(commit=False)
			pnt =  GEOSGeometry(entry.location)
            pnt.srid = 4326
            pnt.transform(26986)
            entry.location = pnt
            entry.save()            
            return HttpResponseRedirect('/') # Redirect after POST
            # return HttpResponse('ok')
	else:
		form = ProjectForm(request.POST)
	
	return render_to_response('projects/add.html', 
								{'form': form,}, 
								context_instance=RequestContext(request))
    
def edit(request, project_id):
    
    # ProjectForm = forms.form_for_model(Project)
    
    project = Project.objects.transform(4326).get(pk = project_id)
    
    if request.method == 'POST': # If the form has been submitted...
        form = ProjectForm(request.POST, instance=project) # A form bound to the POST data        
        
        if form.is_valid(): # All validation rules pass
            
            # TODO: send email
            
            entry = form.save(commit=False)
            
            
            # request.user.id
            
            # l = request.POST['location']
            
            # form.comments = 'nada'
            
            # l = 'POINT (-70.9704880433288707 42.3640977778136687)'
            
            # entry.taz = Taz.objects.get(geometry__contains=l)
            
            pnt =  GEOSGeometry(entry.location)
            pnt.srid = 4326
            # ct = CoordTransform(SpatialReference(900913), SpatialReference(26986))
            pnt.transform(26986)
            
            # entry.location = pnt
            
            # entry.comments = pnt
            entry.location = pnt
            
            # entry.taz = Taz.objects.get(geometry__contains=pnt)
             
            
            # form.location = pnt
            # form.taz = p.taz

            
#            l = 'POINT (236106.3766999999934342 891587.2271999999647960)'
            # t = Taz.objects.get(geometry__contains=pnt)
#            form.taz_id = '395'

            # ct = CoordTransform(SpatialReference(900913), SpatialReference(26986))
            # l.transform(ct)
            
            entry.save()            
            return HttpResponseRedirect('/') # Redirect after POST
            # return HttpResponse('ok')
    else:
        form = ProjectForm(instance=project)
        
    return render_to_response('projects/edit.html', 
                              {'project': project,
                               'form': form,}, 
                              context_instance=RequestContext(request))
