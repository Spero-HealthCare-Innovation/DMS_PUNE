from django.db import models
from admin_web.models import *
from django_enumfield import enum
from django.contrib.auth.hashers import make_password

class status_enum(enum.Enum):
	Active = 1
	Inactive = 2
	Delete = 3
	__default__ = Active
 
class device_platform(enum.Enum):
    Androind = 1
    IOS = 2
    
class Vehical_base_location(models.Model):
    bs_id = models.AutoField(primary_key=True)
    bs_name = models.CharField(max_length=100)
    bs_state = models.ForeignKey(DMS_State, on_delete=models.CASCADE)
    bs_district = models.ForeignKey(DMS_District, on_delete=models.CASCADE)
    bs_tahsil = models.ForeignKey(DMS_Tahsil, on_delete=models.CASCADE)
    bs_city = models.ForeignKey(DMS_City, on_delete=models.CASCADE)
    bs_ward = models.ForeignKey(DMS_Ward, on_delete=models.CASCADE)
    bs_address = models.TextField(null=True)
    bs_lat = models.DecimalField(max_digits=9,decimal_places=6, null=True)
    bs_long = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    status = enum.EnumField(status_enum, null=True)
    bs_added_by = models.CharField(max_length=200, null=True)
    bs_added_date = models.DateTimeField(auto_now_add=True)
    bs_modify_by = models.CharField(max_length=200, null=True)
    bs_modify_date = models.DateTimeField(auto_now=True)

# Create your models here.
class Vehical(models.Model):
    veh_id = models.AutoField(primary_key=True)
    veh_number = models.CharField(max_length=50, null=True)
    veh_default_mobile = models.CharField(max_length=15, null=True)
    veh_base_location = models.ForeignKey(Vehical_base_location, on_delete=models.CASCADE, null=True)
    veh_hash = models.TextField(null=True)
    veh_state = models.ForeignKey(DMS_State, on_delete=models.CASCADE, null=True)
    veh_district = models.ForeignKey(DMS_District ,on_delete=models.CASCADE, null=True)
    veh_tahsil = models.ForeignKey(DMS_Tahsil, on_delete=models.CASCADE, null=True)
    veh_city = models.ForeignKey(DMS_City, on_delete=models.CASCADE, null=True)
    veh_app_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    veh_app_log = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    veh_gps_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    veh_gps_log = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    veh_address = models.TextField(null=True)
    veh_ward_id = models.ForeignKey(DMS_Ward, on_delete=models.CASCADE, null=True)
    status = enum.EnumField(status_enum, null=True)
    vehis_login = models.BooleanField(default=False)
    veh_added_by = models.CharField(max_length=100, null=True)
    veh_added_date = models.DateTimeField(auto_now_add=True)
    veh_modify_by = models.CharField(max_length=100, null=True)
    veh_modify_date = models.DateTimeField(auto_now=True)
     
    def save(self, *args, **kwargs):
        self.veh_number = make_password(self.veh_default_mobile)
        return super().save(*args, **kwargs)
    
class Device_version(models.Model):
    device_id = models.AutoField(primary_key=True)
    os_version = models.CharField(max_length=9, null=True)
    device_platform = enum.EnumField(device_platform, null=True)
    app_version = models.CharField(max_length=9, null=True)
    device_timezone = models.CharField(max_length=50, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    device_token = models.TextField(null=True)
    model_name = models.CharField(max_length=200, null=True)
    status = enum.EnumField(status_enum, null=True)
    
class Device_version_info(models.Model):
    device_version_id = models.AutoField(primary_key=True)
    os_name = enum.EnumField(device_platform, null=True)
    os_version = models.CharField(max_length=100, null=True)
    app_location = models.URLField(max_length=500, null=True)
    app_current_version = models.CharField(max_length=50, null=True)
    app_compulsory_version = models.CharField(max_length=50, null=True)
    status = enum.EnumField(status_enum)
    added_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    