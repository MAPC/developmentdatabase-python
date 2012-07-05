def bing_api_key(request):
    from django.conf import settings
    return { 'bing_api_key' : settings.BING_API_KEY }