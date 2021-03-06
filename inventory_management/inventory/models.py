from django.db import models
from django.db.models import Count, Q
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

from django.core.validators import RegexValidator
from .validators import validate_mac_address, validate_file_extension
from django.urls import reverse

import os


PM_COVERAGE = (
	('Annual', 'Annual'),
	('Semi-Annual', 'Semi-Annual'),
	('Quarterly', 'Quarterly'),
	)

AREA = [
	('Provincial', 'Provincial'),
	('Metro Manila', 'Metro Manila'),
	('Head Office', 'Head Office'),
	]

STATUS = (
    ('Covered by MA', 'Covered by MA'),
    ('Not Covered by MA', 'Not Covered by MA'),
    )

PM_TYPE = (
    ('1st PM', '1st PM'),
    ('2nd PM', '2nd PM'),
    ('3rd PM', '3rd PM'),
    ('4th PM', '4th PM'),
    )

#used to classify the display of forms
MACHINE_CLASS = (
    ('CPU', 'CPU'),
    ('Laptop', 'Laptop'),
    ('Printer', 'Printer'),
    )

MONITOR_TYPE = (
    ('LCD', 'LCD'),
    ('CRT', 'CRT'),
    ('LED', 'LED'),
    )

WORKING_CHOICES = (
    ('Y', 'Y'),
    ('N', 'N')
    )

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Please enter alphanumeric characters.')

def update_filename(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = instance.service_report_number + '.' + ext
    return os.path.join("certification_forms/", new_filename)


class ClientProfile(models.Model):

    username = models.OneToOneField(User, on_delete=models.CASCADE)
    client_code = models.CharField(max_length=255, unique=True)
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

    class Meta:
        ordering = ['username']

    def __str__(self):
    	return self.client_code

    def get_client_name(self):
        return self.client_name

class BusinessUnit(models.Model):

    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    business_unit_name = models.CharField(max_length=255) #department/branch
    rc_code = models.CharField(max_length=255, unique=True)
    area = models.CharField(choices=AREA, max_length=50)
    location = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_unit_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_unit_updated')

    class Meta:
        ordering = ['business_unit_name']

    def __str__(self):
    	return self.business_unit_name

class MachineType(models.Model):

    machine_class = models.CharField(choices=MACHINE_CLASS, max_length=50)
    machine_type_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='machine_type_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='machine_type_updated')

    class Meta:
        ordering = ['machine_type_name']

    def __str__(self):
    	return self.machine_type_name

class Brand(models.Model):

    brand_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='brand_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='brand_updated')

    class Meta:
        ordering = ['brand_name']

    def __str__(self):
    	return self.brand_name

class Model(models.Model):

    machine_type = models.ForeignKey(MachineType, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    model_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='model_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='model_updated')

    class Meta:
        ordering = ['model_name']

    def __str__(self):
    	return self.model_name

class OperatingSystem(models.Model):

    os_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='os_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='os_updated')

    class Meta:
        ordering = ['os_name']

    def __str__(self):
    	return self.os_name

class OfficeApplication(models.Model):

    office_app_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='office_app_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='office_app_updated')

    class Meta:
        ordering = ['office_app_name']

    def __str__(self):
    	return self.office_app_name

class Processor(models.Model):

    processor_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processor_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processor_updated')

    class Meta:
        ordering = ['processor_name']

    def __str__(self):
    	return self.processor_name

class TotalRam(models.Model):

    total_ram_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='total_ram_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='total_ram_updated')

    class Meta:
        ordering = ['total_ram_name']

    def __str__(self):
    	return self.total_ram_name

class HddSize(models.Model):

    hdd_size_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hdd_size_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hdd_size_updated')

    class Meta:
        ordering = ['hdd_size_name']

    def __str__(self):
    	return self.hdd_size_name


class Unit(models.Model):

    area = models.CharField(choices=AREA, max_length=50)
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)
    machine_type = models.ForeignKey(MachineType, on_delete=models.PROTECT)
    machine_brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='machine_brand')
    model = models.ForeignKey(Model, on_delete=models.PROTECT)
    serial_number = models.CharField(max_length=15, unique=True, validators=[alphanumeric]) #UNIQUE #MAXLENGTH=15 #ALPHANUMERIC
    computer_tag = models.CharField(max_length=10, unique=True, validators=[alphanumeric]) #UNIQUE #MAXLENGTH=10 #ALPHANUMERIC null=True
    mst_tag = models.CharField(max_length=255, blank=True, null=True)
    user = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)

    #details for CPU and LAPTOP only
    operating_system = models.ForeignKey(OperatingSystem, on_delete=models.PROTECT, blank=True, null=True)
    office_application = models.ForeignKey(OfficeApplication, on_delete=models.PROTECT, blank=True, null=True)
    host_name = models.CharField(max_length=255, blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True, validators=[validate_mac_address])
    ip_address = models.GenericIPAddressField(blank=True, null=True) #NUMBERS AND PERIOD ONLY
    processor = models.ForeignKey(Processor, on_delete=models.PROTECT, blank=True, null=True)
    total_ram = models.ForeignKey(TotalRam, on_delete=models.PROTECT, blank=True, null=True)
    hdd_size = models.ForeignKey(HddSize, on_delete=models.PROTECT, blank=True, null=True)
    monitor_type = models.CharField(choices=MONITOR_TYPE, max_length=10, blank=True, null=True)
    monitor_brand = models.ForeignKey(Brand, on_delete=models.PROTECT, blank=True, null=True, related_name='monitor_brand')
    monitor_size = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.TextField(max_length=500, blank=True, null=True)
    working = models.CharField(choices=WORKING_CHOICES, max_length=1, default='Y')
    status = models.CharField(choices=STATUS, max_length=30)

    active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unit_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unit_updated')

    history = HistoricalRecords(cascade_delete_history=True)

    class Meta:
        ordering = ['-created_at']
        permissions = [
            ('can_view_unit_list', 'Can view unit list'),
            ('can_soft_delete_unit', 'Can soft delete unit'),
            ('can_view_unit_history', 'Can view unit history')   
        ]

    def __str__(self):
    	return self.serial_number

    def get_absolute_url(self):
        return reverse('inventory:unit-view', kwargs={'pk': self.pk})

    def get_active_units(request):
        if ClientProfile.objects.filter(username=request.user).exists():
            return Unit.objects.filter(active=True, business_unit__client=request.user.clientprofile)
        return Unit.objects.filter(active=True)

    def get_total_count(client=None, business_unit=None, area=None):
        return Unit.objects.filter(dynamic_filter_pm(client, business_unit, area)).count()

    def get_unit_num_per_branch(client=None):
        units = Unit.objects.values('business_unit')\
                            .filter(active=True, business_unit__client=client)\
                            .annotate(unit_per_bu=Count('business_unit'))

        return units

# set as base dynamic filtering for class PreventiveMaintenance
def dynamic_filter_pm(client, business_unit, area):

    filter_ = Q(active=True)

    if client:
        filter_ &= Q(business_unit__client=client)
    if business_unit:
        filter_ &= Q(business_unit=business_unit)
    if area:
        filter_ &= Q(business_unit__area=area)

    return filter_

class PreventiveMaintenance(models.Model):

    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)
    service_report_number = models.CharField(max_length=255, unique=True, null=True)
    pm_type = models.CharField(choices=PM_TYPE, max_length=50)
    target_date = models.DateField()
    target_time = models.TimeField()
    #actual_date = models.DateField()
    pm_date_done = models.DateField(blank=True, null=True)
    pm_done = models.BooleanField(default=False)
    assigned_personnel = models.CharField(max_length=100)
    remarks = models.TextField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)
    attachment = models.FileField(upload_to=update_filename, validators=[validate_file_extension], blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pm_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pm_updated')

    #history = HistoricalRecords(cascade_delete_history=True)

    class Meta:
        ordering = ['-created_at']
        permissions = [
            ('can_view_pm_list', 'Can view pm list'),
            ('can_view_units_per_pm', 'Can view units per pm'),
            ('can_mark_as_done', 'Can mark as done per pm'),
            ('can_soft_delete_pm', 'Can soft delete pm'),
            ('can_generate_certification_form', 'Can generate certification form'),
            ('can_generate_pm_attachment', 'Can generate pm attachment'),
            ('can_generate_excel_report_count', 'Can generate excel report count'),
    ]

    def __str__(self):
        return self.business_unit.business_unit_name

    def filename(self):
        return os.path.basename(self.attachment.name)

    def get_absolute_url(self):
        return reverse('inventory:pm-view', kwargs={'pk': self.pk})

    def get_active_pms(status=None, client=None):

        filter_ = Q(active=True)

        if status == 'Done':
            pm_done = True
            filter_ &= Q(pm_done=pm_done)
        elif status == 'Pending':
            pm_done = False
            filter_ &= Q(pm_done=pm_done)

        if client:
            filter_ &= Q(business_unit__client=client)            
            
        return PreventiveMaintenance.objects.filter(filter_)

    def get_total_count(client=None, business_unit=None, area=None):
        return PreventiveMaintenance.objects.filter(dynamic_filter_pm(client, business_unit, area)).count()

    def get_total_count_per_status(client=None, business_unit=None, area=None):
        return PreventiveMaintenance.objects.values('pm_done')\
                                            .filter(dynamic_filter_pm(client, business_unit, area))\
                                            .order_by('pm_done')\
                                            .annotate(status_count=Count('pm_done'))

    def get_pending_pm(number_to_retrive=5, client=None, business_unit=None, area=None):

        filter_ = dynamic_filter_pm(client, business_unit, area)
        filter_ &= Q(pm_done=False)

        return PreventiveMaintenance.objects.filter(filter_)\
                                            .order_by('-target_date', '-target_time')[:number_to_retrive]

class PmUnitHistory(models.Model):

    preventive_maintenance = models.ForeignKey(PreventiveMaintenance, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    pm_done = models.BooleanField(default=False)
    pm_date_done = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(max_length=500, blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pmhistory_updated', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ('can_add_remarks_per_pm', 'Can add extra remarks per pm')
    ]

class EmailTemplate(models.Model):

    used_for = models.CharField(max_length=255, unique=True)
    subject = models.CharField(max_length=255)
    body = models.TextField(max_length=1500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_updated')

    def __str__(self):
        return self.used_for