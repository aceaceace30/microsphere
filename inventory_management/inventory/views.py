from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string, get_template
from django.contrib.messages.views import SuccessMessageMixin

from .models import Unit, PreventiveMaintenance, MachineType, PmUnitHistory, ClientProfile,\
BusinessUnit, Model, EmailTemplate
from django.db.models import Count, Q
from .forms import PreventiveMaintenanceForm, UnitForm, PreventiveMaintenanceEditForm

from django.conf import settings
from django.core.mail import send_mail

from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

import datetime

from .utils import Render
from xhtml2pdf import pisa

import os

@login_required
def load_business_units(request):
	area = request.GET.get('area')
	business_unit_id = request.GET.get('business_unit')
	business_units = BusinessUnit.objects.filter(area=area, active=True)

	if business_unit_id:
		business_unit = business_units.get(pk=business_unit_id)

	context = {
		'business_units':business_units,
		'business_unit':business_unit if business_unit_id else None
	}

	return render(request, 'inventory/includes/unit/partial_business_unit_dropdown.html', context)

@login_required
def load_brand_choices(request):

	machine_type = request.GET.get('machine_type')
	machine_brand_id = request.GET.get('machine_brand')
	brands = None

	if machine_brand_id:
		brand = Brand.objects.get(pk=machine_brand_id, active=True)

	if machine_type:
		query = "SELECT id, model.brand_id, brand.brand_name FROM\
				(SELECT DISTINCT brand_id FROM inventory_model WHERE machine_type_id={0} and active=1) AS model\
				INNER JOIN inventory_brand AS brand\
				ON model.brand_id = brand.id".format(machine_type)

		brands = Model.objects.raw(query)



	context = {
		'brands':brands,
		'brand':brand if machine_brand_id else None
	}

	return render(request, 'inventory/includes/unit/partial_brand_dropdown.html', context)

@login_required
def load_model_choices(request):

	machine_type = request.GET.get('machine_type')
	machine_brand = request.GET.get('machine_brand')
	model_id = request.GET.get('model')
	models = None

	if model_id:
		model = Model.objects.get(pk=model_id, active=True)

	if machine_type and machine_brand:
		models = Model.objects.filter(machine_type=machine_type, brand=machine_brand, active=True)

	context = {
		'models':models,
		'model':model if model_id else None
	}

	return render(request, 'inventory/includes/unit/partial_model_dropdown.html', context)

class UnitListJson(BaseDatatableView):
	# The model we're going to show
	model = Unit

	# define the columns that will be returned
	columns = ['client', 'business_unit', 'serial_number', 'status']

	# define column names that will be used in sorting
	# order is important and should be same as order of columns
	# displayed by datatables. For non sortable columns use empty
	# value like ''
	order_columns = ['business_unit__client', 'business_unit', 'serial_number', 'status']

	# set max limit of records returned, this is used to protect our site if someone tries to attack our site
	# and make it return huge amount of data
	max_display_length = 500

	def get_initial_queryset(self):
		return Unit.get_active_units(self.request)

	def render_column(self, row, column):
		# We want to render client as a custom column
		if column == 'client':
			# escape HTML for security reasons
			return escape('{0}'.format(row.business_unit.client))
		else:
			return super(UnitListJson, self).render_column(row, column)

	# def filter_queryset(self, qs):
	# 	# use parameters passed in GET request to filter queryset

	# 	# simple example:
	# 	# search = self.request.GET.get('search[value]', None)
	# 	# if search:
	# 	# 	qs = qs.filter(name__istartswith=search)

	# 	# more advanced example using extra parameters
	# 	# filter_serial_number = self.request.GET.get('serial_number', None)

	# 	# if filter_serial_number:
	# 	# 	qs = qs.filter(serial_number=filter_serial_number)

	# 	filter_client = self.request.GET.get('Client', None)

	# 	print('Client:', filter_client)

	# 	if filter_client:
	# 		qs = qs.filter(business_unit__client_client_code__istartswith=upper(filter_client))

	# 	return qs

class UnitListView(LoginRequiredMixin, ListView):
	login_url = settings.LOGOUT_REDIRECT_URL
	template_name = 'inventory/unit/unit_list.html'
	context_object_name = 'units'
	ordering = ['business_unit__client', 'business_unit']

	def get_queryset(self):
		return Unit.get_active_units(self.request)

class UnitCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
	permission_required = 'inventory.add_unit'
	login_url = settings.LOGOUT_REDIRECT_URL
	template_name = 'inventory/unit/unit_create.html'
	model = Unit
	form_class = UnitForm
	success_message = 'Unit has been added.'

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		form.instance.updated_by = self.request.user
		return super(UnitCreateView, self).form_valid(form)

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

#permission not working
class UnitDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
	permission_required = 'inventory.view_unit'
	login_url = settings.LOGOUT_REDIRECT_URL
	template_name = 'inventory/unit/unit_view.html'
	context_object_name = 'unit'

	def get_object(self):
		pk = self.kwargs.get('pk')
		return get_object_or_404(Unit, pk=pk, active=True)

def unit_delete(request, pk):
	unit = get_object_or_404(Unit, pk=pk, active=True)
	template_name = 'inventory/unit/unit_delete.html'

	if request.method == 'POST':
		unit.active = False
		unit.save()
		messages.error(request, 'Unit has been deleted.')
		return redirect('inventory:unit-list')
	else:
		context = {
			'unit':unit
		}
	return render(request, template_name, context)

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
		print('Fields:', c.changes)
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
	form_class = PreventiveMaintenanceEditForm
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
		units = Unit.objects.filter(business_unit__pk=pk, active=True)
		self.business_unit_name = units[0].business_unit
		self.client = units[0].business_unit.client
		return units

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['previous'] = self.request.META['HTTP_REFERER']
		context['business_unit_name'] = self.business_unit_name
		context['client'] = self.client
		return context

# def unit_save(request, form, template_name):
# 	data = dict()

# 	render_table_html = 'inventory/includes/unit/partial_unit_list.html'

# 	if request.method == 'POST':
# 		if form.is_valid():

# 			post = form.save(commit=False)

# 			if not post.pk:
# 				post.created_by = request.user
# 			post.updated_by = request.user
# 			post.save()

# 			data['form_is_valid'] = True

# 			units = Unit.get_active_units()
# 			data['html_unit_list'] = render_to_string(render_table_html, {'units': units})
# 		else:
# 			data['form_is_valid'] = False

# 	context = {'form': form}
# 	data['html_form'] = render_to_string(template_name, context, request=request)

# 	return JsonResponse(data)

# @permission_required('inventory.add_unit')
# def unit_create(request):

# 	render_create_html = 'inventory/includes/unit/partial_unit_create.html'

# 	if request.method == 'POST':

# 		form = UnitForm(request.POST)

# 	else:

# 		form = UnitForm()

# 	return unit_save(request, form, render_create_html)


def pm_save(request, form, template_name):
	data = dict()

	render_table_html = 'inventory/includes/pm/partial_pm_list.html'

	if request.method == 'POST':

		# checks if to send an email or not
		sendmail = request.POST.get('sendmail', default=None)

		if form.is_valid():

			emails = form.cleaned_data['emails']
			post = form.save(commit=False)
			post.created_by = request.user
			post.updated_by = request.user

			""" Dynamic part of the email sending. needed to use try catch to handle errors if their is no available 
				data from the database """
			try:
				format_email = EmailTemplate.objects.get(used_for='create pm')
				subject = format_email.subject
			except:
				format_email = None
				subject = 'Microshphere Systems Technology'


			email_message = 'Please be informed that the Preventive Maintenance Activity for\
							 PC and Printers enrolled in <br/>Maintenance Agreement and assigned\
							 to your branch will be scheduled on <u>{0} at {1}</u>.<br/>\
							 Assigned MST Personnel will be: <u>{2}</u>'.format(post.target_date, post.target_time, post.assigned_personnel)

			split_emails = []

			if emails and sendmail:
				if ',' in emails:
					split_emails = emails.split(',')
				else:
					split_emails.append(emails)

				EMAIL_TEMPLATE = render_to_string('inventory/email/pm_create_email_template.html', 
												 {'email_message': email_message,
												  'format_email':format_email,})

				send_mail(subject, '',
					      settings.COMPANY_NAME + ' <' + settings.EMAIL_HOST_USER + '>',
					      split_emails,
					      html_message=EMAIL_TEMPLATE)

			post.save()

			# loop all units to create pm history instance to have a display on pm remarks
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
	pm = get_object_or_404(PreventiveMaintenance, pk=pk, active=True)
	template_name = 'inventory/pm/pm_delete.html'

	if request.method == 'POST':
		pm.active = False
		pm.save()
		messages.error(request, 'PM has been deleted.')
		return redirect('inventory:pm-list')
	else:
		context = {
			'pm':pm
		}
	return render(request, template_name, context)

def add_pm_remarks(request, pk):
	pm_history = get_object_or_404(PmUnitHistory, pk=pk)

	if request.method == 'POST':
		remarks = request.POST.get('remarks', default=None)
		pm_history.remarks = remarks
		pm_history.updated_by = request.user
		pm_history.updated_at = datetime.datetime.now()
		pm_history.save()
		messages.success(request, 'Remarks has been added.')

	return redirect('inventory:unit-view', pm_history.unit.pk)

def mark_as_done(request, pk):
	pm = get_object_or_404(PreventiveMaintenance, pk=pk)
	units = Unit.objects.filter(active=True, business_unit__pk=pm.business_unit.pk)

	if request.method == 'POST':

		emails = request.POST.get('emails', default=None).replace(' ', '')
		service_report_number = request.POST.get('service_report_number', default=None)

		# validation for sr field if blank
		if not service_report_number:
			messages.error(request, 'SR # cannot be blank.')
			return redirect('inventory:pm-view', pk)

		# validation for sr field if exist in database
		if PreventiveMaintenance.objects.filter(service_report_number=service_report_number).exists():
			messages.error(request, 'SR # already exist. Please try a new one.')
			return redirect('inventory:pm-view', pk)

		# if validations passed
		pm.service_report_number = service_report_number
		pm.pm_done = True
		pm.pm_date_done = datetime.datetime.now()
		pm.save()

		# declared empty list to append if the user input a single email
		split_emails = []

		""" if emails exist check if the email field has a comma ',' character to determine if it has
			more than one email to send if it has more than one use the split function to transform it into
			a list else append the single email to the empty list because the send_mail function needed a list
			on the recipient """
		if emails:
			if ',' in emails:
				split_emails = emails.split(',')
			else:
				split_emails.append(emails)

			""" Dynamic part of the email sending. needed to use try catch to handle errors if their is no available 
				data from the database """
			try:
				format_email = EmailTemplate.objects.get(used_for='done pm')
				subject = format_email.subject
			except:
				format_email = None
				subject = settings.COMPANY_NAME

			EMAIL_TEMPLATE = render_to_string('inventory/email/pm_done_email_template.html', 
											 {'units':units,
											  'pm':pm,
											  'format_email':format_email,})

			test_emails = ['michaelababao200@gmail.com', 'marcababao@gmail.com']
			mail_check = send_mail(subject, '', settings.EMAIL_HOST_USER, split_emails, html_message=EMAIL_TEMPLATE)

			if mail_check:
				messages.success(request, 'Email has been sent.')
			else:
				messages.danger(request, 'There was an issue while trying to send the email. Please check your internet connection.')
		else:
			messages.danger(request, 'There was no email input.')

		messages.success(request, 'Preventive maintenance has marked as done.')

	return redirect('inventory:pm-view', pk)

def report_main(request):

	return render(request, 'inventory/report/report_main.html')


# def render_pdf_view(request):
# 	template_path = 'inventory/pdf/preventive_maintenance_certification_form.html'

# 	units = Unit.objects.filter(active=True)
# 	today = datetime.datetime.today()

# 	context = {
# 		'units': units,
# 		'request': request,
# 		'today': today,
# 		'rc_code': units[0].business_unit.rc_code,
# 		'remarks': 'test_remarks',
# 		'company': settings.COMPANY_NAME.upper(),
# 		'address': settings.COMPANY_ADDRESS,
# 		'contact': settings.COMPANY_CONTACT,
# 	}
# 	# Create a Django response object, and specify content_type as pdf
# 	response = HttpResponse(content_type='application/pdf')
# 	response['Content-Disposition'] = 'attachment; filename="report.pdf"'
# 	# find the template and render it.
# 	template = get_template(template_path)
# 	html = template.render(context)

# 	# create a pdf
# 	pisaStatus = pisa.CreatePDF(
# 	html, dest=response, link_callback=link_callback)
# 	# if error then show some funy view
# 	if pisaStatus.err:
# 		return HttpResponse('We had some errors <pre>' + html + '</pre>')
# 	return response

class GeneratePdf(View):

	def get(self, request):
		#print('self: ', self.kwargs)
		#pk = self.kwargs.get('pk')
		#pk=2
		units = Unit.objects.filter(active=True)
		today = datetime.datetime.now()
		context = {
			'units': units,
			'request': request,
			'today': today,
			'rc_code': units[0].business_unit.rc_code,
			'remarks': 'test_remarks',
			'company': settings.COMPANY_NAME.upper(),
			'address': settings.COMPANY_ADDRESS,
			'contact': settings.COMPANY_CONTACT,
		}
		return Render.render('inventory/pdf/preventive_maintenance_certification_form.html', context)



	