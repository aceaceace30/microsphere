from django.shortcuts import render, redirect
from inventory.models import Unit, PreventiveMaintenance

from datetime import datetime

def redirect_to_login(request):
	return redirect('account:login')

def dashboard(request):
	template_name = 'registration/dashboard.html'
	unit_count = Unit.get_total_count()
	pm_count = PreventiveMaintenance.get_total_count()
	pm_count_status = PreventiveMaintenance.get_total_count_per_status()
	pms = PreventiveMaintenance.get_pending_pm(number_to_retrive=5)

	context = {'unit_count':unit_count,
			   'pm_count':pm_count,
			   'pm_count_status':pm_count_status,
			   'pms':pms,
			   'date_today': datetime.now()}

	return render(request, template_name, context)
