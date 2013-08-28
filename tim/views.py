# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template  import RequestContext
from django.http      import Http404, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.gis.geos        import GEOSGeometry
from django.core.exceptions         import FieldError

from development.models import Municipality, Project
from tim.models import ModeratedProject

# decorator to allow MAPC admins only
def all(request):
    """List all projects awaiting moderation"""

    # pending_projects = ModeratedProject.objects.filter(completed=False)
    # pending_projects = [1, 2, 3]

    pending_projects = [
        {'name': '100 Acres',
         'dd_id': '1',
         'proposed_edits':
            {
                'Title': {'current': '100 Acres','proposed': 'Harborlot'},
                'Reported Employment': {'current': 80,'proposed': 100},
            }
        },
        {'name': 'Residences At 8 Winter Street',
         'dd_id': '345',
         'proposed_edits':
            {
                'description': {'current': 'Change office use of floors 3 thru 12 to residnetial with 4-6 units per floor for a total of 40 to 60 units. The conceptual floor plans show studios, 1 BR and 2BR units.','proposed': '3F-12F becoming residential (4-6 units/floor), total 40-60 units. Draft floor plans show studios, 1 BR and 2BR units.'},
                'Project Area': {'current': 12.022202,'proposed': 12.0},
            }
        },
    ]

    return render_to_response('all.html', locals(), context_instance=RequestContext(request))
    

# decorator to allow only Municipal Users for the given municipality
def municipality(request, municipality_name):
    """
    List a municipality's projects awaiting moderation.
    Available only to Municipal Users of the given municipality.
    """

    municipality_name = municipality_name.capitalize()

    try:
        municipality = Municipality.objects.get(name=municipality_name)
    except Municipality.DoesNotExist:
        pass
        # raise Http404
    
    if municipality_name == "Cambridge":
        pending_projects = [1, 2, 3]

    if municipality_name == "Somerville":
        pending_projects = [9, 12, 8]


    return render_to_response('municipality.html', locals(), context_instance=RequestContext(request))
    # return HttpResponse("You are looking at %(municipality)s's projects awaiting moderation." % locals())