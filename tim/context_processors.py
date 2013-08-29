from django.conf import settings

def auth_variables(request):
    if request.user.profile.is_municipal:
        is_municipal = True
    else:
        is_municipal = False


    return {
        'is_municipal': is_municipal
    }