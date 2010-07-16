from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from communitycomments.projects.models import Project, Taz

def index(request):
    project_list = Project.objects.all().order_by('-last_modified')[:25]
    return render_to_response('projects/index.html', {'project_list': project_list})

def community(request, community_name):
    project_list = Project.objects.filter(taz__town_name__iexact=community_name)[:25]
    return render_to_response('projects/community.html', {'project_list': project_list})

def detail(request, project_id):
    p = get_object_or_404(Project, pk=project_id)
    return render_to_response('projects/detail.html', {'project': p})