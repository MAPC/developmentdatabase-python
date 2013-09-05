from django.conf import settings

def auth_variables(request):
    if request.user.is_anonymous():
        return {} # must be a dict
    else:
        return {
            'is_municipal': request.user.profile.is_municipal,
            'is_trusted':   request.user.profile.is_trusted,
        }