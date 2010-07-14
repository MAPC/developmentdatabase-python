from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from communitycomments.projects.models import Project

def index(request):
    latest_project_list = Project.objects.all().order_by('-last_modified')[:5]
    return render_to_response('projects/index.html', {'latest_project_list': latest_project_list})

def detail(request, project_id):
    p = get_object_or_404(Project, pk=project_id)
    return render_to_response('projects/detail.html', {'project': p})