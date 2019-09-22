from django.shortcuts import render
from inventory.models import Unit, PreventiveMaintenance

def dashboard(request):
	template_name = 'registration/dashboard.html'
	unit_count = Unit.get_total_count()
	pm_count = PreventiveMaintenance.get_total_count()
	pm_count_status = PreventiveMaintenance.get_total_count_per_status()

	context = {'unit_count':unit_count,
			   'pm_count':pm_count,
			   'pm_count_status':pm_count_status}

	return render(request, template_name, context)
