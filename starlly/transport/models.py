from datetime import datetime
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import FieldDoesNotExist

# Create your models here.
User = get_user_model()

class Vehicle(TimeStampedModel):
    """ Model for storing Vehicles Details """
    VEHICLEGROUP_CHOICES = Choices(
        ("DMG", "DMG"),
        ("Stockyard", "Stockyard"),
    )
    VEHICLETYPE_CHOICES = Choices(
        ("Tipper", "Tipper"),
        ("Tractor", "Tractor"),
        ("Lorry", "Lorry"),
    )
    INSTALLATIONTYPE_CHOICES = Choices(
        ("New Installation", "New Installation"),
        ("Migration", "Migration"),
        ("Renewal with existing hardware", "Renewal with existing hardware"),
    )
    vehicleNumber = models.CharField("Vehicle Number", max_length=30, null=True, blank=True)
    vehicleStatus = models.CharField("Vehicle Status ", max_length=30, null=True, blank=True)
    vehicleGroup = StatusField("Vehicle Group ", choices_name='VEHICLEGROUP_CHOICES', default="DMG")
    totalPermits = models.IntegerField("Total Permits", null=True, default=0)
    ownerPhone = models.CharField("Owner Phone ", max_length=30,null=True,blank=True)
    licenseStart = models.DateTimeField("License Start Date",null=True,blank=True)
    licenseEnd = models.DateTimeField("License End Date", null=True,blank=True)
    licenseStatus = models.CharField("License Status", max_length=30, null=True)
    capacity = models.FloatField("Capacity ",null=True,default=0)
    vehicleType = StatusField("Vehicle Type",choices_name='VEHICLETYPE_CHOICES', default="Tipper")
    gpsIMEI = models.IntegerField("GPS IMEI",null=True)
    telecomProvider = models.CharField("Telecom Provider",max_length=30, null=True)
    simNo = models.CharField("Sim No",max_length=30, null=True, blank=True)
    registrationDate = models.DateField("Registration Date",auto_now_add=True, null=True)
    installationtype = StatusField("Installation Type",choices_name='INSTALLATIONTYPE_CHOICES', default="New Installation")
    registrationBy = models.CharField("Registration By", max_length=50, null=True,blank=True)
    
    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

    def __str__(self):
        return str(self.vehicleNumber) + " - " + str(self.vehicleStatus)


class PermitTracker(TimeStampedModel):
    """ Model for storing Permit Tracker Details """
    PermitNumber = models.CharField("Permit Number",max_length=30, null=True, blank=True)
    ILMS_number = models.CharField("ILMS Number",max_length=30, null=True, blank=True)
    VehicleNumber = models.ForeignKey(Vehicle, related_name="permit_vehicles",
                on_delete=models.CASCADE, null=True, blank=True)
    PermitStart = models.DateTimeField("Permit Start",null=True,blank=True)
    PermitValidTill = models.DateTimeField("Permit Valid Till",null=True,blank=True)
    LoadingLocation = models.CharField("Loading Location",max_length=30, null=True, blank=True)
    Destination  = models.CharField("Destination",max_length=30, null=True, blank=True)
    Qty = models.FloatField("Qty",null=True, blank=True, default=0)
    Alerts = models.IntegerField("Alerts", null=True, blank=True, default=0)
    
    class Meta:
        verbose_name = "Permit Tracker"
        verbose_name_plural = "Permits Tracker"

    def __str__(self):
        return str(self.PermitNumber) + " - " + str(self.ILMS_number)

    # @property
    # def permit_hours(self):
    #     diff = permit.PermitValidTill - permit.PermitStart
    #     days, seconds = diff.days, diff.seconds
    #     hours = days * 24 + seconds // 3600
    #     return hours

