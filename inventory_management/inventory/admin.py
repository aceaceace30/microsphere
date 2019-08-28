from django.contrib import admin
from .models import ClientProfile, BusinessUnit, MachineType, Brand, Model, OperatingSystem,\
OfficeApplication, Processor, TotalRam, HddSize, Unit

site_header = 'Microsphere Administration'

class ClientProfileAdmin(admin.ModelAdmin):

	readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')

	list_display = ('username', 'client_name', 'client_code', 'pm_coverage',
					'email', 'contact_no', 'date_started', 'active', 'created_at', 'created_by')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

admin.site.register(ClientProfile, ClientProfileAdmin)
admin.site.register(BusinessUnit)
admin.site.register(MachineType)
admin.site.register(Brand)
admin.site.register(Model)
admin.site.register(OperatingSystem)
admin.site.register(OfficeApplication)
admin.site.register(Processor)
admin.site.register(TotalRam)
admin.site.register(HddSize)
admin.site.register(Unit)