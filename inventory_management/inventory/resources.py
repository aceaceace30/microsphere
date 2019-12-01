from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import BusinessUnit, ClientProfile, Unit, MachineType, Brand, Model, OperatingSystem, OfficeApplication,\
Processor, TotalRam, HddSize

from django.contrib.auth.models import User

class ClientProfileResource(resources.ModelResource):

	username = fields.Field(attribute='username', widget=ForeignKeyWidget(User, 'username'), column_name='username')
	created_by = fields.Field(attribute='created_by', widget=ForeignKeyWidget(User, 'username'), column_name='created_by')
	updated_by = fields.Field(attribute='updated_by', widget=ForeignKeyWidget(User, 'username'), column_name='updated_by')

	class Meta:
		model = ClientProfile
		fields = ('username', 'client_code', 'client_name','address',
			      'pm_coverage','contact_no','email','date_started','description',
			      'created_by', 'updated_by')

		import_id_fields = ['username', 'client_code']

		export_order = fields
		skip_unchange = True
		report_skipped = False

	def before_import_row(self, row, **kwargs):
		client = ClientProfile.objects.filter(username__username=row['username'], client_code=row['client_code']).exists()

		if not client:
			row['created_by'] = kwargs['user']
		row['updated_by'] = kwargs['user']

class BusinessUnitResource(resources.ModelResource):

	client = fields.Field(attribute='client',
		                  column_name='client',
		                  widget=ForeignKeyWidget(ClientProfile, 'client_code'))

	created_by = fields.Field(attribute='created_by', widget=ForeignKeyWidget(User, field='username'), column_name='created_by')
	updated_by = fields.Field(attribute='updated_by', widget=ForeignKeyWidget(User, field='username'), column_name='updated_by')

	class Meta:
		model = BusinessUnit
		fields = ('client', 'business_unit_name', 'rc_code', 'area', 'location', 'description', 'created_by', 'updated_by')
		export_order = fields
		import_id_fields = ['rc_code', 'client', 'area']
		skip_unchange = True
		report_skipped = False

	def before_import_row(self, row, **kwargs):
		business_unit = BusinessUnit.objects.filter(rc_code=row['rc_code'],
												    client__client_code=row['client'],
												    area=row['area']).exists()

		if not business_unit:
			row['created_by'] = kwargs['user']
		row['updated_by'] = kwargs['user']

class UnitResource(resources.ModelResource):

	business_unit = fields.Field(attribute='business_unit',
		                  column_name='rc_code',
		                  widget=ForeignKeyWidget(BusinessUnit, 'rc_code'))

	machine_type = fields.Field(attribute='machine_type',
		                  column_name='machine_type',
		                  widget=ForeignKeyWidget(MachineType, 'machine_type_name'))

	machine_brand = fields.Field(attribute='machine_brand',
		                  column_name='machine_brand',
		                  widget=ForeignKeyWidget(Brand, 'brand_name'))

	model = fields.Field(attribute='model',
		                  column_name='model',
		                  widget=ForeignKeyWidget(Model, 'model_name'))

	operating_system = fields.Field(attribute='operating_system',
		                  column_name='operating_system',
		                  widget=ForeignKeyWidget(OperatingSystem, 'os_name'))

	office_application = fields.Field(attribute='office_application',
		                  column_name='office_application',
		                  widget=ForeignKeyWidget(OfficeApplication, 'office_app_name'))

	processor = fields.Field(attribute='processor',
		                  column_name='processor',
		                  widget=ForeignKeyWidget(Processor, 'processor_name'))

	total_ram = fields.Field(attribute='total_ram',
		                  column_name='total_ram',
		                  widget=ForeignKeyWidget(TotalRam, 'total_ram_name'))

	hdd_size = fields.Field(attribute='hdd_size',
		                  column_name='hdd_size',
		                  widget=ForeignKeyWidget(HddSize, 'hdd_size_name'))

	monitor_brand = fields.Field(attribute='monitor_brand',
		                  column_name='monitor_brand',
		                  widget=ForeignKeyWidget(Brand, 'brand_name'))

	created_by = fields.Field(attribute='created_by', widget=ForeignKeyWidget(User, 'username'), column_name='created_by')
	updated_by = fields.Field(attribute='updated_by', widget=ForeignKeyWidget(User, 'username'), column_name='updated_by')

	class Meta:
		model = Unit
		exclude = ('id', 'active', 'created_at', 'updated_at')

		export_order = ('area','business_unit','machine_type',
						'machine_brand','model','serial_number',
						'computer_tag','mst_tag','user','designation',
						'operating_system','office_application','host_name',
						'mac_address','ip_address','processor','total_ram',
						'hdd_size','monitor_type','monitor_brand','monitor_size',
						'remarks','working','status')

		import_id_fields = ['serial_number', 'business_unit']
		skip_unchange = True
		report_skipped = False

	def before_import_row(self, row, **kwargs):
		unit = Unit.objects.filter(serial_number=row['serial_number'],
								   business_unit__rc_code=row['rc_code']).exists()

		if not unit:
			row['created_by'] = kwargs['user']
		row['updated_by'] = kwargs['user']

class MachineTypeResource(resources.ModelResource):

	created_by = fields.Field(attribute='created_by', widget=ForeignKeyWidget(User, field='username'), column_name='created_by')
	updated_by = fields.Field(attribute='updated_by', widget=ForeignKeyWidget(User, field='username'), column_name='updated_by')

	class Meta:
		model = MachineType
		fields = ('id', 'machine_class','machine_type_name','description','created_by','updated_by')
		export_order = fields

		skip_unchange = True
		report_skipped = False

	def before_import_row(self, row, **kwargs):
		machine_type = BusinessUnit.objects.filter(pk=row['id']).exists()

		if not machine_type:
			row['created_by'] = kwargs['user']
		row['updated_by'] = kwargs['user']

class BrandResource(resources.ModelResource):

	created_by = fields.Field(attribute='created_by', widget=ForeignKeyWidget(User, field='username'), column_name='created_by')
	updated_by = fields.Field(attribute='updated_by', widget=ForeignKeyWidget(User, field='username'), column_name='updated_by')

	class Meta:
		model = Brand
		fields = ('id', 'brand_name','description', 'created_by', 'updated_by')
		export_order = fields

		skip_unchange = True
		report_skipped = False

	def before_import_row(self, row, **kwargs):
		brand = Brand.objects.filter(pk=row['id']).exists()

		if not brand:
			row['created_by'] = kwargs['user']
		row['updated_by'] = kwargs['user']

class ModelResource(resources.ModelResource):

	machine_type = fields.Field(attribute='machine_type',
			                   column_name='machine_type',
			                   widget=ForeignKeyWidget(MachineType, 'machine_type_name'))

	brand = fields.Field(attribute='brand',
		                 column_name='brand',
		                 widget=ForeignKeyWidget(Brand, 'brand_name'))

	created_by = fields.Field(attribute='created_by', widget=ForeignKeyWidget(User, field='username'), column_name='created_by')
	updated_by = fields.Field(attribute='updated_by', widget=ForeignKeyWidget(User, field='username'), column_name='updated_by')

	class Meta:
		model = Model
		fields = ('id', 'machine_type', 'brand', 'model_name', 'description', 'created_by', 'updated_by')
		export_order = fields

		skip_unchange = True
		report_skipped = False

	def before_import_row(self, row, **kwargs):
		model = Model.objects.filter(pk=row['id']).exists()

		if not model:
			row['created_by'] = kwargs['user']
		row['updated_by'] = kwargs['user']

class OperatingSystemResource(resources.ModelResource):

	created_by = fields.Field(attribute='created_by', widget=ForeignKeyWidget(User, field='username'), column_name='created_by')
	updated_by = fields.Field(attribute='updated_by', widget=ForeignKeyWidget(User, field='username'), column_name='updated_by')

	class Meta:
		model = OperatingSystem
		fields = ('id', 'os_name','description', 'created_by', 'updated_by')
		export_order = fields

		skip_unchange = True
		report_skipped = False

	def before_import_row(self, row, **kwargs):
		operating_system = OperatingSystem.objects.filter(pk=row['id']).exists()

		if not operating_system:
			row['created_by'] = kwargs['user']
		row['updated_by'] = kwargs['user']

class OfficeApplicationResource(resources.ModelResource):

	created_by = fields.Field(attribute='created_by', widget=ForeignKeyWidget(User, field='username'), column_name='created_by')
	updated_by = fields.Field(attribute='updated_by', widget=ForeignKeyWidget(User, field='username'), column_name='updated_by')

	class Meta:
		model = OfficeApplication
		fields = ('id', 'office_app_name','description', 'created_by', 'updated_by')
		export_order = fields

		skip_unchange = True
		report_skipped = False

	def before_import_row(self, row, **kwargs):
		office_application = OfficeApplication.objects.filter(pk=row['id']).exists()

		if not office_application:
			row['created_by'] = kwargs['user']
		row['updated_by'] = kwargs['user']

class ProcessorResource(resources.ModelResource):

	created_by = fields.Field(attribute='created_by', widget=ForeignKeyWidget(User, field='username'), column_name='created_by')
	updated_by = fields.Field(attribute='updated_by', widget=ForeignKeyWidget(User, field='username'), column_name='updated_by')

	class Meta:
		model = Processor
		fields = ('id', 'processor_name','description', 'created_by', 'updated_by')
		export_order = fields

		skip_unchange = True
		report_skipped = False

	def before_import_row(self, row, **kwargs):
		processor = Processor.objects.filter(pk=row['id']).exists()

		if not processor:
			row['created_by'] = kwargs['user']
		row['updated_by'] = kwargs['user']


class TotalRamResource(resources.ModelResource):

	created_by = fields.Field(attribute='created_by', widget=ForeignKeyWidget(User, field='username'), column_name='created_by')
	updated_by = fields.Field(attribute='updated_by', widget=ForeignKeyWidget(User, field='username'), column_name='updated_by')

	class Meta:
		model = TotalRam
		fields = ('id', 'total_ram_name','description', 'created_by', 'updated_by')
		export_order = fields

		skip_unchange = True
		report_skipped = False

	def before_import_row(self, row, **kwargs):
		total_ram = TotalRam.objects.filter(pk=row['id']).exists()

		if not total_ram:
			row['created_by'] = kwargs['user']
		row['updated_by'] = kwargs['user']


class HddSizeResource(resources.ModelResource):

	created_by = fields.Field(attribute='created_by', widget=ForeignKeyWidget(User, field='username'), column_name='created_by')
	updated_by = fields.Field(attribute='updated_by', widget=ForeignKeyWidget(User, field='username'), column_name='updated_by')

	class Meta:
		model = HddSize
		fields = ('id', 'hdd_size_name','description', 'created_by', 'updated_by')
		export_order = fields

		skip_unchange = True
		report_skipped = False

	def before_import_row(self, row, **kwargs):
		hdd_size = HddSize.objects.filter(pk=row['id']).exists()

		if not hdd_size:
			row['created_by'] = kwargs['user']
		row['updated_by'] = kwargs['user']