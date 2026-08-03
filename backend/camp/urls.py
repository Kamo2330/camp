from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def api_root(_request):
    return JsonResponse(
        {
            'message': 'Camp Security API',
            'frontend': 'http://localhost:3000',
            'endpoints': {
                'health': '/api/health/',
                'site': '/api/site/',
                'services': '/api/services/',
                'admin': '/admin/',
            },
        }
    )


urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
]
