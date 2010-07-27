from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm
from communitycomments.projects.models import Project, ProjectForm, Taz

from django.template import RequestContext

# required for finding taz for project location
from django.contrib.gis.geos import GEOSGeometry

# GeoJSON output
from vectorformats.Formats import Django, GeoJSON

def index(request):
    # project_list = Project.objects.transform(900913).all().order_by('-last_modified')[:25]

	if request.user.is_authenticated():
		user_town = request.user.profile.town.town_name
		project_list = Project.objects.transform(900913).filter(taz__town_name__iexact=user_town)
		return render_to_response('projects/index.html', 
	                              {'project_list': project_list,
	                               'town': user_town,}, 
	                              context_instance=RequestContext(request))
	else:
		return render_to_response('projects/index.html', context_instance=RequestContext(request))

def community(request, community_name):
	if request.user.is_authenticated():
		project_list = Project.objects.transform(900913).filter(taz__town_name__iexact=community_name)
		return render_to_response('projects/community.html', 
                              {'project_list': project_list}, 
                              	context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def detail(request, project_id):
	if request.user.is_authenticated():
		project = get_object_or_404(Project, pk=project_id)
		return render_to_response('projects/detail.html', 
								{'project': project}, 
								context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')
	

def project_geojson(request, project_id):
	if request.user.is_authenticated():
		project = Project.objects.transform(4326).get(pk = project_id)
		return render_to_response('projects/project.geojson', 
								{'project': project}, 
								context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

def add(request):
	if request.user.is_authenticated():
		user_town = request.user.profile.town.town_name
		
		if request.method == 'POST':
			form = ProjectForm(request.POST)
			if form.is_valid():
				entry = form.save(commit=False)
				pnt =  GEOSGeometry(entry.location)
				pnt.srid = 4326
				pnt.transform(26986)
				entry.location = pnt
				entry.save()
				return HttpResponseRedirect('/')
		else:
			form = ProjectForm()
			town = Taz.objects.filter(town_name=user_town).collect()
			town.transform(4326)
			map_center = town.centroid
			return render_to_response('projects/add.html', 
							{'form': form,
							'map_center': map_center,
							'town': user_town}, 
							context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')
    
def edit(request, project_id):
	if request.user.is_authenticated():
		# ProjectForm = forms.form_for_model(Project)

		project = Project.objects.transform(4326).get(pk = project_id)
    
		if request.method == 'POST': # If the form has been submitted...
			form = ProjectForm(request.POST, instance=project) # A form bound to the POST data        
			if form.is_valid(): # All validation rules pass
				# TODO: send notification email
				entry = form.save(commit=False)
				pnt =  GEOSGeometry(entry.location)
				pnt.srid = 4326
				pnt.transform(26986)
				entry.location = pnt
				entry.save()            
				return HttpResponseRedirect('/')
		else:
			form = ProjectForm(instance=project)
			
		return render_to_response('projects/edit.html', 
								{'project': project,
								'form': form,}, 
								context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')
								
def town_taz_geojson(request, community_name):
	if request.user.is_authenticated():
		taz_list = Taz.objects.transform(900913).filter(town_name__iexact=community_name) 
		# http://stackoverflow.com/questions/3034482/rendering-spatial-data-of-geoqueryset-in-a-custom-view-on-geodjango
		djf = Django.Django(geodjango='geometry', properties=['taz_id'])
		geoj = GeoJSON.GeoJSON()
		taz_geojson = geoj.encode(djf.decode(taz_list))
	
		return render_to_response('projects/taz.geojson', 
								{'taz_list': taz_list,
								'taz_geojson': taz_geojson}, 
								context_instance=RequestContext(request))
	else:
		return HttpRespondRedirect('/')