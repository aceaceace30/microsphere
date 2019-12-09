from django.shortcuts import render, redirect
from inventory.models import Unit, PreventiveMaintenance, ClientProfile, MachineType, BusinessUnit, Processor,\
OperatingSystem, TotalRam, HddSize, OfficeApplication

from account.forms import DashboardFilterForm

from django.contrib.auth.decorators import permission_required, login_required

from django.db.models import Count, Q
from datetime import datetime

from django.conf import settings

def redirect_to_login(request):
	return redirect('account:login')

@login_required
def dashboard(request):
	template_name = 'registration/dashboard.html'

	# checks if account login is a client else microsphere account
	client = request.user.clientprofile if ClientProfile.objects.filter(username=request.user).exists() else None
	# set business_unit value to None to avoid errors on filter on get request
	business_unit = None
	area = None

	if request.method == 'POST':

		# instance for filtering (client - set queryset based on login account else view all)
		filter_form = DashboardFilterForm(client, request.POST)

		if filter_form.is_valid():
			business_unit = filter_form.cleaned_data['business_unit']
			client = filter_form.cleaned_data['client']
			area = filter_form.cleaned_data['area']
	else:
		# kwargs initial - to set initial value of dropdown for client else display default
		filter_form = DashboardFilterForm(client, initial = {'client': client.pk if client else None})

	# get total unit count
	unit_count = Unit.get_total_count(client=client, business_unit=business_unit, area=area)

	# get pm status
	pm_count = PreventiveMaintenance.get_total_count(client=client, business_unit=business_unit, area=area)
	pm_count_status = PreventiveMaintenance.get_total_count_per_status(client=client, business_unit=business_unit, area=area)
	pms = PreventiveMaintenance.get_pending_pm(number_to_retrive=5, client=client, business_unit=business_unit, area=area)

	# set base value for filtering
	# did this way because different queryset needs different filtering
	filter_business_unit = Q(active=True) & Q(unit__active=True) & Q(client__active=True)
	filter_base = Q(active=True) & Q(unit__active=True)
	filter_static = Q(active=True)

	# checks if client is not None and concat filtering
	if client:
		filter_business_unit &= Q(client=client)
		filter_base &= Q(unit__business_unit__client=client)
		filter_static &= Q(business_unit__client=client)

	# checks if business_unit is not None and concat filtering
	if business_unit:
		filter_business_unit &= Q(business_unit_name=business_unit)
		filter_base &= Q(unit__business_unit=business_unit)
		filter_static &= Q(business_unit=business_unit)

	# checks if area is not None and concat filtering
	if area:
		filter_business_unit &= Q(area=area)
		filter_base &= Q(unit__business_unit__area=area)
		filter_static &= Q(area=area)

	# define queryset to display on each card
	unit_count_per_bu = BusinessUnit.objects.filter(filter_business_unit).annotate(unit_count=Count('unit'))
	machine_type_count = MachineType.objects.filter(filter_base).annotate(machine_count=Count('unit'))
	processor_count = Processor.objects.filter(filter_base).annotate(processor_count=Count('unit'))
	os_count = OperatingSystem.objects.filter(filter_base).annotate(os_count=Count('unit'))
	ram_count = TotalRam.objects.filter(filter_base).annotate(ram_count=Count('unit'))
	hdd_count = HddSize.objects.filter(filter_base).annotate(hdd_count=Count('unit'))
	monitor_type_count = Unit.objects.filter(filter_static)\
	                                 .values('monitor_type')\
									 .order_by('monitor_type')\
									 .annotate(monitor_type_count=Count('monitor_type'))
	brand_count = Unit.objects.filter(filter_static)\
	                          .values('machine_brand')\
	                          .order_by('machine_brand')\
	                          .annotate(brand_count=Count('machine_brand'))
	office_app_count = OfficeApplication.objects.filter(filter_base).annotate(office_app_count=Count('unit'))

	context = {'unit_count':unit_count,
			   'pm_count':pm_count,
			   'pm_count_status':pm_count_status,
			   'pms':pms,
			   'unit_count_per_bu':unit_count_per_bu,
			   'machine_type_count':machine_type_count,
			   'processor_count':processor_count,
			   'os_count':os_count,
			   'ram_count':ram_count,
			   'hdd_count':hdd_count,
			   'monitor_type_count':monitor_type_count,
			   'office_app_count':office_app_count,
			   'filter_form':filter_form,
			   'company_name':settings.COMPANY_NAME,
			   'date_today': datetime.now()}

	return render(request, template_name, context)
