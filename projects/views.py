from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from communitycomments.projects.models import Project, ProjectForm, Taz

from django.template import RequestContext

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
    
def edit(request, project_id):
    p = Project.objects.transform(900913).get(pk = project_id)
    form = ProjectForm(instance=p)
    return render_to_response('projects/edit.html', 
                              {'project': p,
                               'form': form,}, 
                              context_instance=RequestContext(request))