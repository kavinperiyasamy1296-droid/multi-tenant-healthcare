from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Patient, Tenant
from .serializers import PatientSerializer, TenantSerializer


class TenantListView(APIView):
    def get(self, request):
        tenants = Tenant.objects.using("default").all()
        return Response(TenantSerializer(tenants, many=True).data)


class PatientListView(APIView):
    def get(self, request):
        patients = Patient.objects.using(request.tenant_database).all().order_by("-created_at")
        return Response(PatientSerializer(patients, many=True).data)

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = Patient.objects.using(request.tenant_database).create(
            **serializer.validated_data
        )
        return Response(PatientSerializer(patient).data, status=201)
