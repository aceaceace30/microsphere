import re

from django.db import models
from django.contrib.auth.models import User

from django.core.validators import RegexValidator, validate_ipv4_address
from .validators import validate_mac_address


PM_COVERAGE = (
	('Annual', 'Annual'),
	('Semi-Annual', 'Semi-Annual'),
	('Quarterly', 'Quarterly')
	)

AREA = (
	('Provincial', 'Provincial'),
	('Metro Manila', 'Metro Manila'),
	('Head Office', 'Head Office'),
	)

STATUS = (
    ('Covered by MA', 'Covered by MA'),
    ('Not Covered by MA', 'Not Covered by MA'),
    )

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Please enter alphanumeric characters.')

class ClientProfile(models.Model):

    username = models.OneToOneField(User, on_delete=models.CASCADE)
    client_code = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    pm_coverage = models.CharField(choices=PM_COVERAGE, max_length=50)
    contact_no = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    date_started = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_updated')

    def __str__(self):
    	return self.client_code

class BusinessUnit(models.Model):

    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    business_unit_name = models.CharField(max_length=255)
    rc_code = models.CharField(max_length=255, unique=True)
    area = models.CharField(choices=AREA, max_length=50)
    location = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_unit_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_unit_updated')

    def __str__(self):
    	return self.business_unit_name

class MachineType(models.Model):

    machine_type_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='machine_type_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='machine_type_updated')

    def __str__(self):
    	return self.machine_type_name

class Brand(models.Model):

    brand_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='brand_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='brand_updated')

    def __str__(self):
    	return self.brand_name

class Model(models.Model):

    model_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='model_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='model_updated')

    def __str__(self):
    	return self.model_name

class OperatingSystem(models.Model):

    os_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='os_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='os_updated')

    def __str__(self):
    	return self.os_name

class OfficeApplication(models.Model):

    office_app_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='office_app_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='office_app_updated')

    def __str__(self):
    	return self.office_app_name

class Processor(models.Model):

    processor_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processor_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processor_updated')

    def __str__(self):
    	return self.processor_name

class TotalRam(models.Model):

    total_ram_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='total_ram_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='total_ram_updated')

    def __str__(self):
    	return self.total_ram_name

class HddSize(models.Model):

    hdd_size_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hdd_size_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hdd_size_updated')

    def __str__(self):
    	return self.hdd_size_name

class Unit(models.Model):

    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)
    machine_type = models.ForeignKey(MachineType, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=15, unique=True, validators=[alphanumeric]) #UNIQUE #MAXLENGTH=15 #ALPHANUMERIC
    computer_tag = models.CharField(max_length=10, unique=True, validators=[alphanumeric]) #UNIQUE #MAXLENGTH=10 #ALPHANUMERIC null=True
    mst_tag = models.CharField(max_length=255, blank=True, null=True)
    user = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    operating_system = models.ForeignKey(OperatingSystem, on_delete=models.CASCADE)
    office_application = models.ForeignKey(OfficeApplication, on_delete=models.CASCADE)
    host_name = models.CharField(max_length=255, blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True, validators=[validate_mac_address])
    ip_address = models.CharField(max_length=20, validators=[validate_ipv4_address]) #NUMBERS AND PERIOD ONLY
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
    total_ram = models.ForeignKey(TotalRam, on_delete=models.CASCADE)
    hdd_size = models.ForeignKey(HddSize, on_delete=models.CASCADE)
    remarks = models.TextField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unit_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unit_updated')

    def __str__(self):
    	return self.serial_number

class PreventiveMaintenance(models.Model):

    service_report_number = models.CharField(max_length=255)
    target_date = models.DateField()
    actual_date = models.DateField()
    pm_date_done = models.DateField()
    status = models.BooleanField(default=False)
    remarks = models.TextField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pm_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pm_updated')

    def __str__(self):
        return self.number