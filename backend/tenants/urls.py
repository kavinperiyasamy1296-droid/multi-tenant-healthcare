from django.urls import path
from .views import PatientListView, TenantListView

urlpatterns = [
    path("tenants/", TenantListView.as_view()),
    path("patients/", PatientListView.as_view()),
]
