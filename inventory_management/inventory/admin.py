from django.contrib import admin
from .models import ClientProfile

class ClientProfileAdmin(admin.ModelAdmin):

	exclude = ('created_by', 'updated_by')

	list_display = ('user', 'client_name', 'code', 'email', 'active',
					'created_by', 'created_at', 'updated_by', 'updated_at')

	def save_model(self, request, obj, form, change):

		if not obj.pk:
			obj.created_by = request.user

		obj.updated_by = request.user
		obj.save()

admin.site.register(ClientProfile, ClientProfileAdmin)
