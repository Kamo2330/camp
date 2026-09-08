import os

from django.contrib import admin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import include, path

FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')


def api_root(request):
    if 'text/html' in request.headers.get('Accept', ''):
        return HttpResponseRedirect(FRONTEND_URL)
    return JsonResponse(
        {
            'message': 'Camp Security API',
            'frontend': FRONTEND_URL,
            'endpoints': {
                'health': '/api/health/',
                'site': '/api/site/',
                'services': '/api/services/',
                'chat': '/api/chat/',
                'admin': '/admin/',
            },
        }
    )


urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
]
