from django.db import models
from django.contrib.auth.models import User

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

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #change the name to username
    client_name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    pm_coverage = models.CharField(choices=PM_COVERAGE, max_length=50)
    contact_no = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    date_started = models.DateField(null=True, blank=True)
    remarks = models.TextField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_updated')

    def __str__(self):
    	return self.client_name

"""class Unit(models.Model):

	area = models.CharField(choices=AREA, max_length=50)
	business_unit = #ForeignKey
	location = models.CharField(max_length=255)
	machine_type = #ForeignKey
	brand = #ForeignKey
	model = #ForeignKey
	serial_number = #UNIQUE #MAXLENGTH=15 #ALPHANUMERIC
	computer_tag = #UNIQUE #MAXLENGTH=10 #ALPHANUMERIC null=True
	mst_tag = #UNIQUE
	user = models.CharField(max_length=255)
	designation = models.CharField(max_length=255)
	operating_system = #ForeignKey
	office_application = #ForeignKey
	host_name = models.CharField(max_length=255, blank=True, null=True)
	mac_address = models.CharField(max_length=255, blank=True, null=True)
	ip_address = models.CharField(max_length=255) #accept numbers and period only
	processor = #ForeignKey
	total_ram = #ForeignKey
	hdd_size = #ForeignKey
	remarks = models.TextField(max_length=500, blank=True, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unit_created')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unit_updated')

    def __str__(self):
    	return self.serial_number"""

