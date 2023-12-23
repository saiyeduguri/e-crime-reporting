from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_cryptography.fields import encrypt

# Specify unique related_names for groups and user_permissions on the Group and Permission models
class GroupOfficer(models.Model):
    officer = models.ForeignKey('Officer', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class PermissionOfficer(models.Model):
    officer = models.ForeignKey('Officer', on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
class OfficerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('groups', 'user_permissions')




class Incident(models.Model):
    class Meta:
        app_label = 'ecr' 
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100) 
    email = models.EmailField()
    phone_number = models.CharField(max_length=128)
    incident_spot = models.CharField(max_length=200)
    zip = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(99999),
            MinValueValidator(10000)
        ]
    )
    date = models.DateField()
    time = models.TimeField()
    victim_details = models.TextField()
    culprit_details = models.TextField()
    status = models.CharField(max_length=100, default="received")

    def __str__(self):
        return f"Incident: {self.name} ({self.type})"

class User(models.Model):
    class Meta:
        app_label = 'ecr' 
    name = models.CharField(max_length=100)
    identity = encrypt(models.CharField(max_length=50, null=True, blank=True))
    password = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField()
    phone_number = encrypt(models.CharField(max_length=128))
    address = encrypt(models.CharField(max_length=200))
    zip = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(99999),
            MinValueValidator(10000)
        ]
    )

class Officer(AbstractUser):
    class Meta:
        app_label = 'ecr' 

    officer_id = models.PositiveIntegerField(default=0000)
    zip = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(99999),
            MinValueValidator(10000)
        ]
    )
    username = models.CharField(max_length=150)

    groups = models.ManyToManyField(Group, related_name='officer_groups', through=GroupOfficer)
    user_permissions = models.ManyToManyField(Permission, related_name='officer_user_permissions', through=PermissionOfficer)
