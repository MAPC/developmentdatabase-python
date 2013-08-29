from django.conf import settings

def auth_variables(request):
    if request.user.groups.filter(name="Municipal Users").count() > 0:
        is_municipal = True
    else:
        is_municipal = False


    return {
        'is_municipal': is_municipal
    }