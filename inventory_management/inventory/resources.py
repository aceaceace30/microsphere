from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import BusinessUnit, ClientProfile
from django.contrib.auth.models import User

class ClientProfileResource(resources.ModelResource):

	#client = fields.Field(attribute='username', widget=ForeignKeyWidget(User, field='username'), column_name='Username')

	class Meta:
		model = ClientProfile
		fields = ('client_code', 'client_name','address',
			      'pm_coverage','contact_no','email','date_started','description')
		export_order = fields

class BusinessUnitResource(resources.ModelResource):

	client = fields.Field(attribute='client',
		                  column_name='client',
		                  widget=ForeignKeyWidget(ClientProfile, 'client_code'))

	class Meta:
		model = BusinessUnit
		fields = ('client', 'business_unit_name', 'rc_code', 'area', 'location', 'description', 'created_by', 'updated_by')
		export_order = fields
		import_id_fields = ['rc_code',]
		skip_unchange = True
		report_skipped = False

	# def before_import_row(self, row, **kwargs):
	# 	business_unit = BusinessUnit.objects.filter(client=row['rc_code']).exists()
	# 	if not business_unit:
	# 		row['created_by'] = kwargs['user'].id
	# 	row['updated_by'] = kwargs['user'].id