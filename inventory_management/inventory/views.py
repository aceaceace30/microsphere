from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin

from .models import Unit, PreventiveMaintenance, MachineType, PmUnitHistory, ClientProfile
from django.db.models import Count
from .forms import PreventiveMaintenanceForm, UnitForm

from django.conf import settings
from django.core.mail import send_mail

import datetime

class UnitListView(LoginRequiredMixin, ListView):
	login_url = settings.LOGOUT_REDIRECT_URL
	template_name = 'inventory/unit/unit_list.html'
	context_object_name = 'units'
	ordering = ['business_unit__client', 'business_unit']

	def get_queryset(self):
		# checks if the user is a client else return all units
		if ClientProfile.objects.filter(username=self.request.user).exists():
			return Unit.objects.filter(active=True, business_unit__client=self.request.user.clientprofile)
		else:
			return Unit.get_active_units()

#permission not working
class UnitDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
	permission_required = 'inventory.view_unit'
	login_url = settings.LOGOUT_REDIRECT_URL
	template_name = 'inventory/unit/unit_view.html'
	context_object_name = 'unit'

	def get_object(self):
		pk = self.kwargs.get('pk')
		return get_object_or_404(Unit, pk=pk, active=True)

@permission_required('inventory.can_view_unit_history')
def unit_history(request, pk):
	template_name = 'inventory/unit/unit_history.html'
	unit = get_object_or_404(Unit, pk=pk, active=True)
	if request.method == 'GET':
		history = Unit.history.filter(id=pk)
		changes = historical_changes(history)
		context = {'changes': changes,
				   'unit': unit}
		return render(request, template_name, context)

def historical_changes(history):
	changes = []

	if history:
		last = history.first()

		for all_changes in range(history.count()):
			new_record, old_record = last, last.prev_record

			if old_record is not None:
				delta = new_record.diff_against(old_record)
				changes.append(delta)
			last = old_record

	for c in changes:
		#print('Fields:', c.changes)
		for field in c.changes:
			#print(field.field)
			print(field.old, field.new)
			#print(field.new)
		#print('Fields', c.changed_fields)

	return changes

def unit_details(request, pk):
	template_name = 'inventory/unit/unit_view.html'
	unit = get_object_or_404(Unit, pk=pk, active=True)
	if request.method == 'GET':
		pm_history = PmUnitHistory.objects.select_related('preventive_maintenance')\
					.filter(unit_id=pk, unit__active=True)\
					.order_by('-preventive_maintenance__target_date')

		context = {'unit': unit,
				   'pm_history': pm_history}

		return render(request, template_name, context)

class UnitUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
	permission_required = 'inventory.change_unit'
	login_url = settings.LOGOUT_REDIRECT_URL
	model = Unit
	form_class = UnitForm
	template_name = 'inventory/unit/unit_edit.html'
	success_message = 'Your changes has been save.'

	def get_object(self):
		pk = self.kwargs.get('pk')
		return get_object_or_404(Unit, pk=pk, active=True)

####################################################################################

class PmListView(LoginRequiredMixin, ListView):
	login_url = settings.LOGOUT_REDIRECT_URL
	template_name = 'inventory/pm/pm_list.html'
	context_object_name = 'pms'

	def get_context_data(self, *args, **kwargs):
		context = super(PmListView, self).get_context_data(*args, **kwargs)
		status = self.request.GET.get('status', default=None)
		context['status'] = status if status else 'All'
		return context

	def get_queryset(self):
		pk = self.kwargs.get('pk')
		status = self.request.GET.get('status', default=None)

		if ClientProfile.objects.filter(username=self.request.user).exists():
			return PreventiveMaintenance.get_active_pms(status=status, client=self.request.user.clientprofile) if status\
					else PreventiveMaintenance.get_active_pms(client=self.request.user.clientprofile)
		else:
			return PreventiveMaintenance.get_active_pms(status=status) if status else PreventiveMaintenance.get_active_pms()
		
class PmDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
	permission_required = 'inventory.view_preventivemaintenance'
	login_url = settings.LOGOUT_REDIRECT_URL
	template_name = 'inventory/pm/pm_view.html'
	context_object_name = 'pm'

	def get_object(self):
		pk = self.kwargs.get('pk')
		return get_object_or_404(PreventiveMaintenance, pk=pk, active=True)

class PmUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
	permission_required = 'inventory.change_preventivemaintenance'
	login_url = settings.LOGOUT_REDIRECT_URL
	model = PreventiveMaintenance
	form_class = PreventiveMaintenanceForm
	template_name = 'inventory/pm/pm_edit.html'
	success_message = 'Your changes has been save.'

	def get_object(self):
		pk = self.kwargs.get('pk')
		return get_object_or_404(PreventiveMaintenance, pk=pk, active=True)

class UnitPerBranch(LoginRequiredMixin, ListView):
	login_url = settings.LOGOUT_REDIRECT_URL
	template_name = 'inventory/unit/unit_list_per_branch.html'
	context_object_name = 'units'

	def get_queryset(self):
		pk = self.kwargs.get('pk')
		return Unit.objects.filter(business_unit__pk=pk, active=True)
	
	# context = {'units': units,
	# 		   'business_unit_name': units[0].business_unit if units else None} #fix this

	# return render(request, template_name, context)

def unit_save(request, form, template_name):
	data = dict()

	render_table_html = 'inventory/includes/unit/partial_unit_list.html'

	if request.method == 'POST':
		if form.is_valid():

			post = form.save(commit=False)

			if not post.pk:
				post.created_by = request.user
			post.updated_by = request.user
			post.save()

			data['form_is_valid'] = True

			units = Unit.get_active_units()
			data['html_unit_list'] = render_to_string(render_table_html, {'units': units})
		else:
			data['form_is_valid'] = False

	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)

	return JsonResponse(data)

@permission_required('inventory.add_unit')
def unit_create(request):

	render_create_html = 'inventory/includes/unit/partial_unit_create.html'

	if request.method == 'POST':

		form = UnitForm(request.POST)

	else:

		form = UnitForm()

	return unit_save(request, form, render_create_html)

def unit_delete(request, pk):
	data = dict()
	unit = get_object_or_404(Unit, pk=pk)

	render_delete_html = 'inventory/includes/unit/partial_unit_delete.html'
	#render_table_html = 'inventory/includes/unit/partial_unit_list.html'

	if request.method == 'POST':
		unit.active = False
		unit.updated_by = request.user
		unit.save()

		return redirect('inventory:unit-list')
		#units = Unit.get_active_units()
		#data['html_unit_list'] = render_to_string(render_table_html, {'units': units})
	else:
		context = {'unit':unit}
		data['html_form'] = render_to_string(render_delete_html, context, request=request)

		return JsonResponse(data)


def pm_save(request, form, template_name):
	data = dict()

	render_table_html = 'inventory/includes/pm/partial_pm_list.html'

	if request.method == 'POST':
		if form.is_valid():

			post = form.save(commit=False)

			if not post.pk:
				post.created_by = request.user
			post.updated_by = request.user
			post.save()
			
			units_per_branch = Unit.objects.values('pk').filter(active=True, business_unit=post.business_unit)

			for unit in units_per_branch:
				PmUnitHistory.objects.create(preventive_maintenance_id=post.pk, unit_id=unit['pk'])

			data['form_is_valid'] = True

			pms = PreventiveMaintenance.get_active_pms()

			data['html_pm_list'] = render_to_string(render_table_html, {'pms': pms})
		else:
			data['form_is_valid'] = False

	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)

	return JsonResponse(data)

@permission_required('inventory.add_preventivemaintenance')
def pm_create(request):

	render_create_html = 'inventory/includes/pm/partial_pm_create.html'

	if request.method == 'POST':

		form = PreventiveMaintenanceForm(request.POST)

	else:

		form = PreventiveMaintenanceForm()

	return pm_save(request, form, render_create_html)

def pm_delete(request, pk):
	data = dict()
	pm = get_object_or_404(PreventiveMaintenance, pk=pk)

	render_delete_html = 'inventory/includes/pm/partial_pm_delete.html'
	render_table_html = 'inventory/includes/pm/partial_pm_list.html'

	if request.method == 'POST':
		pm.active = False
		pm.updated_by = request.user
		pm.save()

		data['form_is_valid'] = True

		pms = PreventiveMaintenance.get_active_pms()
		data['html_pm_list'] = render_to_string(render_table_html, {'pms': pms})
	else:
		data['html_form'] = render_to_string(render_delete_html, {'pm':pm}, request=request)

	return JsonResponse(data)

def add_pm_remarks(request, pk):
	pm_history = get_object_or_404(PmUnitHistory, pk=pk)

	if request.method == 'POST':
		remarks = request.POST.get('remarks', default=None)
		pm_history.remarks = remarks
		pm_history.save()

	return redirect('inventory:unit-view', pm_history.unit.pk)

def mark_as_done(request, pk):
	pm = get_object_or_404(PreventiveMaintenance, pk=pk)
	units = Unit.objects.filter(active=True, business_unit__pk=pm.business_unit.pk)
	SUBJECT = 'Microsphere Systems Technology'
	HEADER = settings.EMAIL_HEADER_MESSAGE

	if request.method == 'POST':

		emails = request.POST.get('emails', default=None).replace(' ', '')
		service_report_number = request.POST.get('service_report_number', default=None)

		if not service_report_number:
			messages.error(request, 'SR # cannot be blank.')
			return redirect('inventory:pm-view', pk)

		if PreventiveMaintenance.objects.filter(service_report_number=service_report_number).exists():
			messages.error(request, 'SR # already exist. Please try a new one.')
			return redirect('inventory:pm-view', pk)

		pm.service_report_number = service_report_number
		pm.pm_done = True
		pm.pm_date_done = datetime.datetime.now()
		pm.save()

		if emails:
			if ',' in emails:
				split_email = emails.split(',')
				emails = ','.join(split_email)

			EMAIL_TEMPLATE = render_to_string('inventory/email/pm_done_email_template.html', 
											 {'units':units,
											  'pm':pm,
											  'HEADER':HEADER})

			send_mail(SUBJECT, '', settings.EMAIL_HOST_USER, [emails], html_message=EMAIL_TEMPLATE)

		messages.success(request, 'Marked as done. Email has been sent.')
	return redirect('inventory:pm-view', pk)

def report_main(request):

	return render(request, 'inventory/report/report_main.html')


	