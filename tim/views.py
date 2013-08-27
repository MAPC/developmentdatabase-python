# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template  import RequestContext
from django.http      import Http404, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.gis.geos        import GEOSGeometry
from django.core.exceptions         import FieldError

from development.models import Project
from tim.models import ModeratedProject

# decorator to allow MAPC admins only
def all(request):
  """List all projects awaiting moderation"""
  return HttpResponse("You are looking at ALL projects awaiting moderation.")

# decorator to allow only Municipal Users for the given municipality
def municipality(request, municipality):
  """
  List a municipality's projects awaiting moderation.
  Available only to Municipal Users of the given municipality.
  """
  municipality = municipality.capitalize()
  return HttpResponse("You are looking at %(municipality)s's projects awaiting moderation." % locals())