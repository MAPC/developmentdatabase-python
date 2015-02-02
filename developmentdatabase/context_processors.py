from django.conf import settings
from development.models import Project

def template_settings(request):
    """ Global values to pass to templates """
    return dict(
        BING_API_KEY = settings.BING_API_KEY,
        WS_MORE_INFO_ICON = settings.WS_MORE_INFO_ICON,
        WS_MORE_INFO_LINK = settings.WS_MORE_INFO_LINK,
        WS_LOGO_URL = settings.WS_LOGO_URL,
        project_count = Project.objects.count(),
    ) 
        
