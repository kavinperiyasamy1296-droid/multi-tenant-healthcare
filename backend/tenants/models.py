from django.db import models


class Tenant(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    name = models.CharField(max_length=120)
    database_name = models.CharField(max_length=80)


class Patient(models.Model):
    full_name = models.CharField(max_length=120)
    date_of_birth = models.DateField()
    status = models.CharField(max_length=20, default="Active")
    created_at = models.DateTimeField(auto_now_add=True)
