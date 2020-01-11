from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse

from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.decorators import login_required
from .decorators import permission_required
from django.contrib import messages

from django.template.loader import render_to_string, get_template

from django.contrib.auth.models import User, Permission

from .models import Unit, PreventiveMaintenance, MachineType, PmUnitHistory, ClientProfile,\
BusinessUnit, Model, EmailTemplate, Processor, OperatingSystem, OfficeApplication, TotalRam, HddSize,\
Brand

from django.db.models import Count, Q

from .forms import PreventiveMaintenanceForm, UnitForm, PreventiveMaintenanceEditForm, NotesForm,\
ServiceReportForm, UploadAttachmentForm

from django.conf import settings
from django.core.mail import send_mail, EmailMessage


from django.utils.decorators import method_decorator

import datetime

from .utils import Render, check_perm
from xhtml2pdf import pisa

import os


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

class UnitDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
	permission_required = 'inventory.view_unit'
	login_url = settings.LOGOUT_REDIRECT_URL
	template_name = 'inventory/unit/unit_view.html'
	context_object_name = 'unit'

	def get_context_data(self, *args, **kwargs):
		pk = self.kwargs.get('pk')
		context = super(UnitDetailView, self).get_context_data(*args, **kwargs)
		context['pm_history'] = PmUnitHistory.objects.select_related('preventive_maintenance')\
													 .filter(unit_id=pk, unit__active=True)\
													 .order_by('-preventive_maintenance__target_date')
		return context

	def get_object(self, *args, **kwargs):
		pk = self.kwargs.get('pk')
		return get_object_or_404(Unit, pk=pk, active=True)

def unit_view_json(request, pk):
	data = dict()

	unit = Unit.objects.filter(pk=pk).values('machine_type__machine_class', 'serial_number', 'computer_tag',
										'mst_tag', 'user', 'designation', 'working', 'status')[:1]

	if request.is_ajax():
		data['unit'] = list(unit)
		return JsonResponse(data)

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
				for c in delta.changes:
					if c.field == 'updated_by':
						data = get_old_new_values(User, 'username', c.old, c.new)
						c.old = data['old']
						c.new = data['new']
					elif c.field == 'business_unit':
						# Special case - to see if client has also been changed.
						old = BusinessUnit.objects.values('business_unit_name', 'client__client_code').get(pk=c.old)
						new = BusinessUnit.objects.values('business_unit_name', 'client__client_code').get(pk=c.new)
						c.old = old['business_unit_name'] + ' ({0})'.format(old['client__client_code'])
						c.new = new['business_unit_name'] + ' ({0})'.format(new['client__client_code'])
					elif c.field == 'machine_type':
						data = get_old_new_values(MachineType, 'machine_type_name', c.old, c.new)
						c.old = data['old']
						c.new = data['new']
					elif c.field == 'machine_brand':
						data = get_old_new_values(Brand, 'brand_name', c.old, c.new)
						c.old = data['old']
						c.new = data['new']
					elif c.field == 'model':
						data = get_old_new_values(Model, 'model_name', c.old, c.new)
						c.old = data['old']
						c.new = data['new']
					elif c.field == 'operating_system':
						data = get_old_new_values(OperatingSystem, 'os_name', c.old, c.new)
						c.old = data['old']
						c.new = data['new']
					elif c.field == 'office_application':
						data = get_old_new_values(OfficeApplication, 'office_app_name', c.old, c.new)
						c.old = data['old']
						c.new = data['new']
					elif c.field == 'processor':
						data = get_old_new_values(Processor, 'processor_name', c.old, c.new)
						c.old = data['old']
						c.new = data['new']
					elif c.field == 'total_ram':
						data = get_old_new_values(TotalRam, 'total_ram_name', c.old, c.new)
						c.old = data['old']
						c.new = data['new']
					elif c.field == 'hdd_size':
						data = get_old_new_values(HddSize, 'hdd_size_name', c.old, c.new)
						c.old = data['old']
						c.new = data['new']
					elif c.field == 'monitor_brand':
						data = get_old_new_values(Brand, 'brand_name', c.old, c.new)
						c.old = data['old']
						c.new = data['new']
					#print("{} changed from {} to {}".format(c.field, c.old, c.new))
				changes.append(delta)
			last = old_record


	return changes

def get_old_new_values(class_, values, old_pk, new_pk):
	data = dict()
	try:
		old = class_.objects.values(values).get(pk=old_pk)
		data['old'] = old[values]
	except:
		data['old'] = 'data has been remove/deleted'

	try:
		old = class_.objects.values(values).get(pk=new_pk)
		data['new'] = old[values]
	except:
		data['new'] = 'data has been remove/deleted'

	return data



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
		status = self.request.GET.get('status', default=None)

		params = dict()

		if status:
			params['status'] = status

		if ClientProfile.objects.filter(username=self.request.user).exists():
			params['client'] = self.request.user.clientprofile

		return PreventiveMaintenance.get_active_pms(**params)

		
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

	def get(self, request, *args, **kwargs):
		if self.get_object().pm_done:
			return redirect('account:dashboard')
		return super().get(request, *args, **kwargs)

	def get_object(self):
		pk = self.kwargs.get('pk')
		return get_object_or_404(PreventiveMaintenance, pk=pk, active=True)

class UnitPerBranch(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	permission_required = 'inventory.can_view_unit_history'
	login_url = settings.LOGOUT_REDIRECT_URL
	template_name = 'inventory/unit/unit_list_per_branch.html'
	context_object_name = 'units'

	def get_queryset(self):
		pk = self.kwargs.get('pk')
		units = PmUnitHistory.objects.filter(preventive_maintenance__pk=self.request.GET.get('pm_pk'))
		business_unit = BusinessUnit.objects.get(pk=pk)
		self.business_unit_name = business_unit.business_unit_name
		self.client = business_unit.client
		return units

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['business_unit_name'] = self.business_unit_name
		context['client'] = self.client
		context['pm_pk'] = self.request.GET.get('pm_pk')
		return context

def pm_save(request, form, template_name):
	data = dict()

	render_table_html = 'inventory/includes/pm/partial_pm_list.html'

	if request.method == 'POST':

		# checks if to send an email or not
		# sendmail = request.POST.get('sendmail', default=None)

		if form.is_valid():

			emails = form.cleaned_data['emails']
			post = form.save(commit=False)

			""" checks first if their is an available unit when creating a pm for that branch 
				do not allow to proceed if their is no unit available. """

			no_unit_exist = Unit.objects.filter(business_unit=post.business_unit).exists()

			if not no_unit_exist:
				data['no_unit_exist'] = True

				return JsonResponse(data)

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

			if emails:
				if ',' in emails:
					split_emails = emails.split(',')
				else:
					split_emails.append(emails)

				EMAIL_TEMPLATE = render_to_string('inventory/email/pm_create_email_template.html', 
												 {'email_message': email_message,
												  'format_email':format_email,})

				email_send = EmailMessage(subject,
									  EMAIL_TEMPLATE,
								      settings.EMAIL_HOST_USER,
								      split_emails,
								      [settings.BCC_EMAIL])

				email_send.content_subtype = 'html'
				email_send.send(fail_silently=True)

				# send_mail(subject, '',
				# 	      settings.EMAIL_HOST_USER,
				# 	      split_emails,
				# 	      html_message=EMAIL_TEMPLATE)

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

@login_required
def pm_delete(request, pk):
	pm = get_object_or_404(PreventiveMaintenance, pk=pk, active=True)
	template_name = 'inventory/pm/pm_delete.html'

	if pm.pm_done:
			return redirect('account:dashboard')

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

@login_required
def add_pm_remarks(request, pk):
	data = dict()
	pm_history = get_object_or_404(PmUnitHistory, pk=pk)

	if request.method == 'POST':
		data['is_valid'] = False
		remarks = request.POST.get('remarks', default=None)

		form = NotesForm(request.POST, instance=pm_history)

		if form.is_valid():
			post = form.save(commit=False)
			post.updated_by = request.user
			post.updated_at = datetime.datetime.now()
			post.save()

			pm_history_list = PmUnitHistory.objects.select_related('preventive_maintenance')\
					.filter(unit=pm_history.unit, unit__active=True)\
					.order_by('-preventive_maintenance__target_date')

			user = request.user
			# check user if has permission
			if not user.is_superuser:
				can_add_remarks_per_pm = Permission.objects.filter(Q(user=user) | Q(group__user=user)).distinct()
				can_add_remarks_per_pm = can_add_remarks_per_pm.filter(codename=perm).exists()
			else:
				can_add_remarks_per_pm = True

			context = {'request': request,
					   'can_add_remarks_per_pm': can_add_remarks_per_pm,
					   'pm_history': pm_history_list,}

			data['pm_history_list'] = render_to_string('inventory/includes/unit/partial_pm_history.html', context, request=request)
			data['message'] = 'Notes has been saved.'
			data['is_valid'] = True

	form = NotesForm(instance=pm_history)

	context = {
		'form': form
	}
	data['notes_form'] = render_to_string('inventory/includes/unit/partial_history_form.html', context, request=request)

	return JsonResponse(data)

@login_required
def pm_mark_done(request, pk):
	template_name = 'inventory/pm/pm_mark_done.html'

	pm = get_object_or_404(PreventiveMaintenance, pk=pk)
	units = pm.pmunithistory_set.all()

	if request.method == 'POST':
		data = dict()

		checked_units = request.POST.get('checked_units', default=None)
		unit_list = list()

		if checked_units:
			if ',' in checked_units:
				unit_list = checked_units.split(',')
				unit_list = list(map(int, unit_list))
			else:
				unit_list.append(int(checked_units))

		# units = units.filter(pm_done=False)
		for unit in units:
			if unit.pk in unit_list:
				unit.pm_done = False
				unit.pm_date_done = None
			else:
				unit.pm_done = True
				unit.pm_date_done = datetime.datetime.now()
			unit.save()

		if len(unit_list) == 0 or not unit_list:
			pm.pm_done = True
			pm.pm_date_done = datetime.datetime.now()
			data['pm_overall_done'] = True
			form = str(ServiceReportForm(instance=pm))
			data['form'] = form
			message = 'All units under this pm has been inspected. Please set Service report #.'
		else:
			pm.pm_done = False
			pm.pm_date_done = None
			data['pm_overall_done'] = False
			message = 'PM has been saved.'

		pm.save()

		data['is_valid'] = True
		data['message'] = message

		return JsonResponse(data)

	context = { 'pm': pm,
				'units': units, }

	return render(request, template_name, context)

@login_required
def save_service_report_no(request, pk):
	data = dict()
	pm = get_object_or_404(PreventiveMaintenance, pk=pk)

	if request.method == 'POST':
		form = ServiceReportForm(request.POST, instance=pm)

		if form.is_valid():
			form.save()
			data['is_valid'] = True
			data['message'] = 'Service report has been saved.'

		else:
			data['is_valid'] = False
			data['form'] = str(form)

	return JsonResponse(data)

@login_required
def check_all_unit_done(request, pk):
	data = dict()
	pm = get_object_or_404(PreventiveMaintenance, pk=pk)

	if request.method == 'GET':
		if pm.pm_done and not pm.service_report_number:
			for history in pm.pmunithistory_set.all():
				if history.pm_done == False:
					data['pm_overall_done'] = False
					break
				else:
					data['pm_overall_done'] = True
					form = str(ServiceReportForm(instance=pm))
					data['form'] = form
					data['message'] = 'All units under this pm has been inspected. Please set Service report #.'

	return JsonResponse(data)

@login_required
def pm_send_email(request, pk):
	data = dict()

	if request.method == 'POST':

		emails = request.POST.get('emails', default=None).replace(' ', '')

		# which columns does the table contains
		checked_cols = request.POST.get('checked_cols', default=None)

		# split the checked cols to a python list
		table_columns = checked_cols.split(', ')

		# declared empty list to append if the user input a single email
		split_emails = []

		""" if emails exist check if the email field has a comma ',' character
			to determine if it has more than one email to send if it has more
			than one use the split function to transform it into a list else append
			the single email to the empty list because the send_mail function
			needed a list on the recipient. """
		if emails:
			if ',' in emails:
				split_emails = emails.split(',')
			else:
				split_emails.append(emails)

			# query all the units
			pm = get_object_or_404(PreventiveMaintenance, pk=pk)
			units = pm.pmunithistory_set.all()

			""" Dynamic part of the email sending.
				needed to use try catch to handle
				errors if their is no available 
				data from the database. """
			try:
				format_email = EmailTemplate.objects.get(used_for='done pm')
				subject = format_email.subject
			except:
				format_email = None
				subject = settings.COMPANY_NAME

			EMAIL_TEMPLATE = render_to_string('inventory/email/pm_done_email_template.html', 
											 {'units':units,
											  'pm':pm,
											  'table_columns': table_columns,
											  'format_email':format_email,})

			email_send = EmailMessage(subject,
									  EMAIL_TEMPLATE,
								      settings.EMAIL_HOST_USER,
								      split_emails,
								      [settings.BCC_EMAIL])

			email_send.content_subtype = 'html'
			email_send.send(fail_silently=True)

			# mail_check = send_mail(subject, '',
			# 					   settings.EMAIL_HOST_USER,
			# 					   split_emails,
			# 					   html_message=EMAIL_TEMPLATE)

			if email_send:
				data['message'] = 'Email has been sent.'
				data['email_sent'] = True
			else:
				data['message'] = 'There was an issue while trying to send the email.\
								   Make sure you have an internet connection.'
				data['email_sent'] = False

		return JsonResponse(data)

def pm_upload_attachment(request, pk):
	data = dict()
	pm = get_object_or_404(PreventiveMaintenance, pk=pk)

	if request.method == 'POST':
		form = UploadAttachmentForm(request.POST, request.FILES, instance=pm)

		if form.is_valid():
			form.save()
			#data['is_valid'] = True
			#data['message'] = 'Upload successful.'
			messages.success(request, 'Upload successful.')
			return redirect('inventory:pm-view', pm.pk)
		else:
			messages.error(request, 'Invalid file format. Only accepts .pdf, .doc, .docx, .xlsx, .xls files.')
			return redirect('inventory:pm-view', pm.pk)
	else:
		form = UploadAttachmentForm(instance=pm)

	context = {'form': form,
			   'pm': pm}

	data['html_form'] = render_to_string('inventory/includes/pm/partial_upload_attachment.html', context, request=request)

	return JsonResponse(data)


class GenerateCertificationForm(LoginRequiredMixin, PermissionRequiredMixin, View):
	login_url = settings.LOGOUT_REDIRECT_URL
	permission_required = 'inventory.can_generate_certification_form'

	def get(self, request, *args, **kwargs):
		pm_pk = self.kwargs.get('pk')

		pm = get_object_or_404(PreventiveMaintenance, pk=pm_pk, active=True)
		#for history in pm.pmunithistory_set.all():

		#units = business_unit.unit_set.filter(active=True)
		business_unit_name = pm.business_unit.business_unit_name #business_unit.business_unit_name
		rc_code = pm.business_unit.rc_code
		today = datetime.datetime.now()

		file_name = 'Certification-Form-{0} ({1})'.format(business_unit_name, rc_code)

		context = {
			'pm': pm,
			'request': request,
			'today': None,
			'business_unit_name': business_unit_name,
			'rc_code': rc_code,
			'company': settings.COMPANY_NAME.upper(),
			'address': settings.COMPANY_ADDRESS,
			'contact': settings.COMPANY_CONTACT,

			# used to create line over signature because
			# this library doesn't support 'text-decorator:overline' in CSS

			'line_spacing': '&nbsp;' * 51
		}

		return Render.render('inventory/pdf/preventive_maintenance_certification_form.html', file_name, context)



	