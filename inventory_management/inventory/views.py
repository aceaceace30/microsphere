from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Unit, PreventiveMaintenance
from .forms import UnitForm

def get_active_units():
	return Unit.objects.filter(active=True)

def get_all_units():
	return Unit.objects.all()

class UnitListView(LoginRequiredMixin, ListView):
	# see django docs on how to use generic CBV:ListView

	# override login_url variable in LoginRequiredMixin class
	login_url = '/accounts/login/'

	# change context name
	# default is 'object_list'	
	context_object_name = 'units'

	# set pagination
	paginate_by = 50

	# override get_queryset method in ListView Class
	def get_queryset(self):
		return get_active_units()

class PmListView(LoginRequiredMixin, ListView):

	# override login_url variable in LoginRequiredMixin class
	login_url = '/accounts/login/'

	context_object_name = 'pms'

	paginate_by = 50

	def get_queryset(self):
		return PreventiveMaintenance.objects.all()

def unit_save(request, form, template_name):
	data = dict()

	render_table_html = 'inventory/includes/table_unit_list.html'

	if request.method == 'POST':
		if form.is_valid():

			post = form.save(commit=False)
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

	render_create_html = 'inventory/includes/partial_unit_create.html'

	if request.method == 'POST':

		form = UnitForm(request.POST)

	else:

		form = UnitForm()

	return unit_save(request, form, render_create_html)

def unit_edit(request, pk):

	unit = get_object_or_404(Unit, pk=pk)

	render_edit_html = 'inventory/includes/partial_unit_edit.html'

	if request.method == 'POST':

		form = UnitForm(request.POST, instance=unit)

	else:

		form = UnitForm(instance=unit)

	return unit_save(request, form, render_edit_html)

def unit_delete(request, pk):
	data = dict()
	unit = get_object_or_404(Unit, pk=pk)

	render_delete_html = 'inventory/includes/partial_unit_delete.html'
	render_table_html = 'inventory/includes/table_unit_list.html'

	if request.method == 'POST':
		unit.active = False
		unit.save()

		data['form_is_valid'] = True

		units = get_active_units()
		data['html_unit_list'] = render_to_string(render_table_html, {'units': units})
	else:
		context = {'unit':unit}
		data['html_form'] = render_to_string(render_delete_html, context, request=request)

	return JsonResponse(data)



	