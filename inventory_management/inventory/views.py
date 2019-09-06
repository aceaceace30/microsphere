from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin

from .models import Unit, PreventiveMaintenance, MachineType
from .forms import PreventiveMaintenanceForm, UnitForm

from django.conf import settings

import datetime

def get_active_units():
	return Unit.objects.filter(active=True)

def get_active_pms():
	return PreventiveMaintenance.objects.filter(active=True)

class UnitListView(LoginRequiredMixin, ListView):
	login_url = settings.LOGOUT_REDIRECT_URL
	template_name = 'inventory/unit/unit_list.html'
	context_object_name = 'units'
	queryset = get_active_units()

class UnitDetailView(LoginRequiredMixin, DetailView):
	login_url = settings.LOGOUT_REDIRECT_URL
	template_name = 'inventory/unit/unit_view.html'
	context_object_name = 'unitwqe'

	def get_object(self):
		pk = self.kwargs.get('pk')
		return get_object_or_404(Unit, pk=pk, active=True)

class UnitUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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
	queryset = get_active_pms()

class PmDetailView(LoginRequiredMixin, DetailView):
	login_url = settings.LOGOUT_REDIRECT_URL
	template_name = 'inventory/pm/pm_view.html'
	context_object_name = 'pm'

	def get_object(self):
		pk = self.kwargs.get('pk')
		return get_object_or_404(PreventiveMaintenance, pk=pk, active=True)

class PmUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	login_url = settings.LOGOUT_REDIRECT_URL
	model = PreventiveMaintenance
	form_class = PreventiveMaintenanceForm
	template_name = 'inventory/pm/pm_edit.html'
	success_message = 'Your changes has been save.'

	def get_object(self):
		pk = self.kwargs.get('pk')
		return get_object_or_404(PreventiveMaintenance, pk=pk, active=True)


def units_per_business_unit(request, pk):

	units = Unit.objects.filter(active=True, business_unit__pk=pk)
	template_name = 'inventory/unit_list_per_branch.html'

	context = {'units': units,
			   'business_unit_name': units[0].business_unit if units else None} #fix this

	return render(request, template_name, context)

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

			units = get_active_units()
			data['html_unit_list'] = render_to_string(render_table_html, {'units': units})
		else:
			data['form_is_valid'] = False

	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)

	return JsonResponse(data)

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
	render_table_html = 'inventory/includes/unit/partial_unit_list.html'

	if request.method == 'POST':
		unit.active = False
		unit.updated_by = request.user
		unit.save()

		data['form_is_valid'] = True

		units = get_active_units()
		data['html_unit_list'] = render_to_string(render_table_html, {'units': units})
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

			data['form_is_valid'] = True

			pms = get_active_pms()
			data['html_pm_list'] = render_to_string(render_table_html, {'pms': pms})
		else:
			data['form_is_valid'] = False

	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)

	return JsonResponse(data)

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

		pms = get_active_pms()
		data['html_pm_list'] = render_to_string(render_table_html, {'pms': pms})
	else:
		context = {'pm':pm}
		data['html_form'] = render_to_string(render_delete_html, context, request=request)

	return JsonResponse(data)

def tag_pm_done_or_undone(request, pk):
	data = dict()
	pm = get_object_or_404(PreventiveMaintenance, pk=pk)

	render_tag_html = 'inventory/includes/pm/partial_pm_tag.html'
	render_table_html = 'inventory/includes/pm/partial_pm_list.html'

	if request.method == 'POST':
		pm.pm_done=True
		pm.pm_date_done=datetime.datetime.now()
		pm.updated_by=request.user
		pm.updated_at=datetime.datetime.now()
		pm.save()

		data['form_is_valid'] = True

		pms = get_active_pms()
		data['html_pm_list'] = render_to_string(render_table_html, {'pms': pms})
	else:
		context = {'pm':pm}
		data['html_form'] = render_to_string(render_tag_html, context, request=request)

	return JsonResponse(data)




	