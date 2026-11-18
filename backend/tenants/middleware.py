from django.conf import settings
from django.http import JsonResponse


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant_id = request.headers.get("X-Tenant", "tenant-a")
        database = settings.TENANT_DATABASES.get(tenant_id)

        if tenant_id != "" and not database:
            return JsonResponse({"detail": "Unknown tenant"}, status=400)

        request.tenant_id = tenant_id
        request.tenant_database = database
        return self.get_response(request)
