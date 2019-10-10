from django.shortcuts import render, redirect
from inventory.models import Unit, PreventiveMaintenance, ClientProfile, MachineType

from datetime import datetime

def redirect_to_login(request):
	return redirect('account:login')

def dashboard(request):
	template_name = 'registration/dashboard.html'

	client = request.user.clientprofile if ClientProfile.objects.filter(username=request.user).exists() else None

	unit_count = Unit.get_total_count(client=client)
	pm_count = PreventiveMaintenance.get_total_count(client=client)
	pm_count_status = PreventiveMaintenance.get_total_count_per_status(client=client)
	pms = PreventiveMaintenance.get_pending_pm(number_to_retrive=5, client=client)
	machine_type_count = Unit.get_machine_type_count_per_client(client=client)
	pc_and_laptop_hardware_count = Unit.pc_and_laptop_hardware_count(client=client)

	#print(machine_type_count)

	context = {'unit_count':unit_count,
			   'pm_count':pm_count,
			   'pm_count_status':pm_count_status,
			   'pms':pms,
			   'machine_type_count':machine_type_count,
			   'pc_and_laptop_hardware_count':pc_and_laptop_hardware_count,
			   'date_today': datetime.now()}

	return render(request, template_name, context)
