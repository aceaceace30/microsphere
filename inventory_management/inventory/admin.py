from django.contrib import admin
from .models import ClientProfile, BusinessUnit, MachineType, Brand, Model, OperatingSystem,\
OfficeApplication, Processor, TotalRam, HddSize, Unit, PreventiveMaintenance, EmailTemplate
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from django_summernote.admin import SummernoteModelAdmin

class ClientProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	list_display = ('username', 'client_name', 'client_code', 'pm_coverage',
					'email', 'contact_no', 'date_started', 'active')

	search_fields = ('username__username', 'client_code', 'client_name', 'pm_coverage',
					'email', 'contact_no', 'date_started', 'active',
					'created_by__username', 'updated_by__username')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

admin.site.register(ClientProfile, ClientProfileAdmin)

class BusinessUnitAdmin(ImportExportModelAdmin, admin.ModelAdmin):

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	list_display = ('client', 'business_unit_name', 'rc_code', 'area',
					'location', 'active')

	search_fields = ('client__client_name', 'client__client_code', 'business_unit_name',
					'rc_code', 'area', 'location', 'active',
					'created_by__username', 'updated_by__username')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

admin.site.register(BusinessUnit, BusinessUnitAdmin)

class UnitHistoryAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):

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

	list_filter = ('business_unit__client', 'area', 'business_unit', 'machine_type', 'machine_brand', 'created_by')

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

class MachineTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):

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

class BrandAdmin(ImportExportModelAdmin, admin.ModelAdmin):

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

class ModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):

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

class OperatingSystemAdmin(ImportExportModelAdmin, admin.ModelAdmin):

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

class OfficeApplicationAdmin(ImportExportModelAdmin, admin.ModelAdmin):

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

class ProcessorAdmin(ImportExportModelAdmin, admin.ModelAdmin):

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

class TotalRamAdmin(ImportExportModelAdmin, admin.ModelAdmin):

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

class HddSizeAdmin(ImportExportModelAdmin, admin.ModelAdmin):

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

class PreventiveMaintenanceAdmin(ImportExportModelAdmin, admin.ModelAdmin):

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

admin.site.register(EmailTemplate, EmailTemplateAdmin)

