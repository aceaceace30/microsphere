from django.contrib import admin
from .models import ClientProfile, BusinessUnit, MachineType, Brand, Model, OperatingSystem,\
OfficeApplication, Processor, TotalRam, HddSize, Unit, PreventiveMaintenance, EmailTemplate

# import export library
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from .resources import BusinessUnitResource, ClientProfileResource, UnitResource, MachineTypeResource,\
BrandResource, ModelResource, OperatingSystemResource, OfficeApplicationResource, ProcessorResource,\
TotalRamResource, HddSizeResource

# simple history library
from simple_history.admin import SimpleHistoryAdmin

# summernote library
from django_summernote.admin import SummernoteModelAdmin

class ClientProfileAdmin(ImportExportModelAdmin):

	resource_class = ClientProfileResource

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	list_display = ('username', 'client_name', 'client_code', 'pm_coverage',
					'email', 'contact_no', 'date_started', 'active')

	search_fields = ('username__username', 'client_code', 'client_name', 'pm_coverage',
					'email', 'contact_no', 'date_started', 'active',
					'created_by__username', 'updated_by__username')

	list_filter = ('active', 'pm_coverage')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

admin.site.register(ClientProfile, ClientProfileAdmin)

class BusinessUnitAdmin(ImportExportModelAdmin):

	resource_class = BusinessUnitResource

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	list_display = ('client', 'business_unit_name', 'rc_code', 'area',
					'location', 'active')

	search_fields = ('client__client_name', 'client__client_code', 'business_unit_name',
					'rc_code', 'area', 'location', 'active',
					'created_by__username', 'updated_by__username')

	list_filter = ('active', 'client', 'area', 'location')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

admin.site.register(BusinessUnit, BusinessUnitAdmin)

class UnitHistoryAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):

	resource_class = UnitResource

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	list_display = ('get_client_code', 'area', 'business_unit', 'get_rc_code', 'machine_type', 'machine_brand',
					'model', 'serial_number', 'computer_tag',
					'mst_tag', 'user', 'designation', 'active', 'created_by', 'created_at')

	search_fields = ('business_unit__client__client_code', 'area', 'business_unit__business_unit_name',
					 	'business_unit__rc_code', 'model__machine_type__machine_type_name', 'model__model_name',
					 	'model__brand__brand_name', 'serial_number', 'computer_tag', 'mst_tag', 'user',
					 	'designation', 'active', 'operating_system__os_name', 'office_application__office_app_name',
						'processor__processor_name', 'total_ram__total_ram_name', 'hdd_size__hdd_size_name',
						'host_name', 'mac_address', 'ip_address', 'remarks',
						'created_by__username', 'updated_by__username')

	list_filter = ('active', 'business_unit__client', 'area',
				   'business_unit', 'machine_type', 'machine_brand',
				   'model', 'operating_system', 'office_application',
				   'processor', 'total_ram', 'hdd_size', 'monitor_type', 'created_by')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

	def get_client_code(self, obj):
		return obj.business_unit.client
	get_client_code.short_description = 'Client'

	def get_rc_code(self, obj):
		return obj.business_unit.rc_code
	get_rc_code.short_description = 'RC Code'

admin.site.register(Unit, UnitHistoryAdmin)

class MachineTypeAdmin(ImportExportModelAdmin):

	resource_class = MachineTypeResource

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	list_display = ('machine_type_name', 'machine_class', 'active', 'created_at')

	search_fields = ('machine_type_name', 'machine_class',
					 'created_by__username', 'updated_by__username')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

admin.site.register(MachineType, MachineTypeAdmin)

class BrandAdmin(ImportExportModelAdmin):

	resource_class = BrandResource

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	list_display = ('brand_name', 'active', 'created_at')

	search_fields = ('brand_name',
					 'created_by__username', 'updated_by__username')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

admin.site.register(Brand, BrandAdmin)

class ModelAdmin(ImportExportModelAdmin):

	resource_class = ModelResource

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	list_display = ('get_machine_type', 'get_brand', 'model_name', 'active', 'created_at')

	search_fields = ('machine_type__machine_type_name', 'brand__brand_name', 'model_name',
					 'created_by__username', 'updated_by__username')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

	def get_machine_type(self, obj):
		return obj.machine_type.machine_type_name
	get_machine_type.short_description = 'Machine Type'

	def get_brand(self, obj):
		return obj.brand.brand_name
	get_brand.short_description = 'Brand'

admin.site.register(Model, ModelAdmin)

class OperatingSystemAdmin(ImportExportModelAdmin):

	resource_class = OperatingSystemResource

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	list_display = ('os_name', 'active', 'created_at')

	search_fields = ('os_name',
					 'created_by__username', 'updated_by__username')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

admin.site.register(OperatingSystem, OperatingSystemAdmin)

class OfficeApplicationAdmin(ImportExportModelAdmin):

	resource_class = OfficeApplicationResource

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	list_display = ('office_app_name', 'active', 'created_at')

	search_fields = ('office_app_name',
				   	 'created_by__username', 'updated_by__username')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

admin.site.register(OfficeApplication, OfficeApplicationAdmin)

class ProcessorAdmin(ImportExportModelAdmin):

	resource_class = ProcessorResource

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	list_display = ('processor_name', 'active', 'created_at')

	search_fields = ('processor_name',
					 'created_by__username', 'updated_by__username')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

admin.site.register(Processor, ProcessorAdmin)

class TotalRamAdmin(ImportExportModelAdmin):

	resource_class = TotalRamResource

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	list_display = ('total_ram_name', 'active', 'created_at')

	search_fields = ('total_ram_name',
					 'created_by__username', 'updated_by__username')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

admin.site.register(TotalRam, TotalRamAdmin)

class HddSizeAdmin(ImportExportModelAdmin):

	resource_class = HddSizeResource

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	list_display = ('hdd_size_name', 'active', 'created_at')

	search_fields = ('hdd_size_name',
					 'created_by__username', 'updated_by__username')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

admin.site.register(HddSize, HddSizeAdmin)

class PreventiveMaintenanceAdmin(ImportExportModelAdmin):

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	list_display = ('get_client_code', 'get_area', 'get_rc_code', 'business_unit', 'service_report_number', 'pm_type', 'target_date', 'target_time',
					'actual_date', 'pm_date_done', 'pm_done', 'active', 'created_by')

	search_fields = ('business_unit__client__client_code', 'business_unit__area', 'business_unit__rc_code',
					 'business_unit__business_unit_name', 'service_report_number', 'pm_type')

	list_filter = ('business_unit__client__client_code', 'business_unit__area', 'business_unit__rc_code', 'business_unit', 'pm_type', 'pm_done', 'created_by')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

	def get_client_code(self, obj):
		return obj.business_unit.client
	get_client_code.short_description = 'Client'

	def get_rc_code(self, obj):
		return obj.business_unit.rc_code
	get_rc_code.short_description = 'RC Code'

	def get_area(self, obj):
		return obj.business_unit.area
	get_area.short_description = 'Area'

admin.site.register(PreventiveMaintenance, PreventiveMaintenanceAdmin)


# Apply summernote to all TextField in model.
class EmailTemplateAdmin(SummernoteModelAdmin):  # instead of ModelAdmin

	summernote_fields = '__all__'

	list_display = ('used_for', 'subject', 'updated_at', 'updated_by')

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	def save_model(self, request, obj, form, change):
		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

	# remove delete selected action
	def get_actions(self, request):
		actions = super().get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	# remove the delete action
	def has_delete_permission(self, request, obj=None):
		return False

admin.site.register(EmailTemplate, EmailTemplateAdmin)

