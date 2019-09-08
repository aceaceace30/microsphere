from django.contrib import admin
from .models import ClientProfile, BusinessUnit, MachineType, Brand, Model, OperatingSystem,\
OfficeApplication, Processor, TotalRam, HddSize, Unit, PreventiveMaintenance
from simple_history.admin import SimpleHistoryAdmin

class ClientProfileAdmin(admin.ModelAdmin):

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

class BusinessUnitAdmin(admin.ModelAdmin):

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

class UnitAdmin(admin.ModelAdmin):

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	list_display = ('get_client_code', 'business_unit', 'get_rc_code', 'machine_type', 'machine_brand',
					'model', 'serial_number', 'computer_tag',
					'mst_tag', 'user', 'designation', 'active')

	search_fields = ('business_unit__client__client_code', 'business_unit__business_unit_name',
					 	'business_unit__rc_code', 'model__machine_type__machine_type_name', 'model__model_name',
					 	'model__brand__brand_name', 'serial_number', 'computer_tag', 'mst_tag', 'user',
					 	'designation', 'active', 'operating_system__os_name', 'office_application__office_app_name',
						'processor__processor_name', 'total_ram__total_ram_name', 'hdd_size__hdd_size_name',
						'host_name', 'mac_address', 'ip_address', 'remarks',
						'created_by__username', 'updated_by__username')

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

	"""def get_machine_type(self, obj):
					return obj.model.machine_type
				get_machine_type.short_description = 'Machine Type'
			
				def get_machine_brand(self, obj):
					return obj.model.brand
				get_machine_brand.short_description = 'Brand'"""

admin.site.register(Unit, SimpleHistoryAdmin)

class MachineTypeAdmin(admin.ModelAdmin):

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

class BrandAdmin(admin.ModelAdmin):

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

class ModelAdmin(admin.ModelAdmin):

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

class OperatingSystemAdmin(admin.ModelAdmin):

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

class OfficeApplicationAdmin(admin.ModelAdmin):

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

class ProcessorAdmin(admin.ModelAdmin):

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

class TotalRamAdmin(admin.ModelAdmin):

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

class HddSizeAdmin(admin.ModelAdmin):

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

class PreventiveMaintenanceAdmin(admin.ModelAdmin):

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	#list_display = ('business_unit', 'service_report_number', 'target_date', 'target_time', 'actual_date',
					#'pm_date_done', 'status', 'created_at', 'active')

	#search_fields = ('business_unit__business_unit_name', 'service_report_number', 'target_date', 'target_time', 'actual_date',
					#'pm_date_done', 'status', 'created_at', 'active',
					#'created_by__username', 'updated_by__username')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

admin.site.register(PreventiveMaintenance, PreventiveMaintenanceAdmin)