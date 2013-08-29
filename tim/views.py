# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template  import RequestContext
from django.http      import Http404, HttpResponse, HttpResponseForbidden
from django.utils.functional import wraps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.gis.geos        import GEOSGeometry
from django.core.exceptions         import FieldError

from development.models import Municipality, Project
from tim.models import ModeratedProject




def correct_municipal_user_or_staff(view):
    """
    Checks to see if the user:
        1) is not anonymous (aka logged in)
        2) is a Municipal User and thus has the power to moderate
        3) is viewing their own municipality.
    If so, it returns to the view the municipality object, from which
    the pending projects may be obtained.
    """
    @wraps(view)
    def inner(request, municipality_name, *args, **kwargs):

        user = request.user
        municipality_name = municipality_name.capitalize()

        if not user.is_staff:
            if user.is_anonymous():
                return HttpResponseForbidden("Log in as a Municipal User to access moderation.")

            if user.groups.filter(name="Municipal Users").count() == 0:
                return HttpResponseForbidden("You are not a Municipal User. If you see this message in error, please contact MAPC.")

            if user.profile.municipality.name != municipality_name:
                return HttpResponseForbidden("You may not view other municipalities' pending edits.")

        try:
            municipality = Municipality.objects.get(name=municipality_name)
        except Municipality.DoesNotExist:
            return Http404

        return view(request, municipality, *args, **kwargs)

    return inner






@staff_member_required
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
    

@correct_municipal_user_or_staff
def municipality(request, municipality):
    """
    List a municipality's projects awaiting moderation.
    Available only to Municipal Users of the given municipality.
    """
    
    if municipality.name == "Cambridge":
        pending_projects = [
            {'name': 'Elm St., #325',
             'dd_id': '1487',
             'proposed_edits':
                {
                    'description': {'current': 'Prior use: vacant','proposed': 'Prior use: empty'},
                    'Reported Employment': {'current': 0, 'proposed': 12},
                }
            },
            {'name': 'Cambridge St., #1066 (Antiques Mall)',
             'dd_id': '1513',
             'proposed_edits':
                {
                    'description': {'current': 'Prior use: retail, warehouse', 'proposed': 'Prior use: retail, warehouse, to be a modern antiques outlet'},
                    'Reported Employment': {'current': 0, 'proposed': 4},
                }
            },
        ]

    if municipality.name == "Somerville":
        pending_projects = [
            {'name': '245 Beacon Street 1',
             'dd_id': '1612',
             'proposed_edits':
                {
                    'Title': {'current': '245 Beacon Street 1','proposed': 'Beacon Historical'},
                    'Project Site Area (acres)': {'current': 0, 'proposed': 0.7},
                }
            },
            {'name': '308 BEACON ST',
             'dd_id': '1407',
             'proposed_edits':
                {
                    'Project Website': {'current': None, 'proposed': 'http://www.308beaconstreet.com'},
                    'Project Site Area (acres)': {'current': 0, 'proposed': 1.1},
                }
            },
        ]

    return render_to_response('municipality.html', locals(), context_instance=RequestContext(request))
