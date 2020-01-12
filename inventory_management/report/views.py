from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.generic import View, TemplateView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import ReportFilterForm, CertficateFilterForm

from inventory.models import MachineType, Processor, TotalRam, HddSize, Unit, PreventiveMaintenance
from django.db.models import Count, Q

from django.contrib.auth.decorators import login_required
from inventory.decorators import permission_required

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from datetime import datetime

from django.conf import settings

from PyPDF2 import PdfFileMerger, PdfFileReader
from io import BytesIO

import xlwt

import os

"""
This class can be a function because its main purpose
is to write the same the logic per sheet for now
but used a class instead for the possibility to be extended in the long run
"""
class ExcelWriter(object):

	def __init__(self, *args, **kwargs):
		pass

	# set up details per sheet
	# workbook = Workbook instance
	# sheet name = name of the sheet
	# columns = columns needed
	# queryset = queryset needed (this needed to be a values_list)
	def create_count_per_item(self, workbook, sheet_name, columns, queryset):

		ws = workbook.add_sheet(sheet_name)
		ws.col(0).width = 13*350

		xlwt.add_palette_colour("custom_blue_color", 0x21) # the second argument must be a number between 8 and 64
		workbook.set_colour_RGB(0x21, 79, 129, 189) # Red — 79, Green — 129, Blue — 189

		header_style = xlwt.easyxf("pattern: pattern solid, fore_colour custom_blue_color; align: vert centre, horiz centre;")
		row_style = xlwt.easyxf("align: vert centre, horiz centre;")

		# set the headers on first row
		row_num = 0

		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num], header_style)

		# Sheet body, remaining rows

		for row in queryset:
			row_num += 1
			for col_num in range(len(row)):
				ws.write(row_num, col_num, row[col_num], row_style)


@login_required
@permission_required('inventory.can_generate_pm_attachment')
def download_pm_attachments(request):
	template_name = 'report/pm_attachments.html'
	if request.method == 'POST':
		form = CertficateFilterForm(request.POST)

		if form.is_valid():
			business_unit = form.cleaned_data['business_unit']

			# get all the pm for a business unit
			# ordering: latest pm date done
			pms = PreventiveMaintenance.objects.filter(business_unit=business_unit).order_by('-pm_date_done')

			# path where to download the save files
			# used business_unit + username of the current user
			# overwrite the file in the temp folder to save space
			filepath_filename = '/media/temp/{0}_{1}.pdf'.format(business_unit, request.user.get_username())
			download_path = settings.BASE_DIR + filepath_filename

			# create instance of PdfFileMerger
			merger = PdfFileMerger()

			"""
				loop through all pms and used the append function of pdf file merger
				which concats pdf
			"""
			for pm in pms:
				if pm.pm_done:
					path_to_file = settings.BASE_DIR + pm.attachment.url
					print(path_to_file)
					merger.append(PdfFileReader(path_to_file))

			# write the merge files and write in the download path
			merger.write(download_path)
			merger.close()

			context = {
				'filepath_filename': filepath_filename
			}
			
			return render(request, 'report/pm_attachments_download.html', context)

	else:
		form = CertficateFilterForm()
		context = {
			'form': form,
		}
		return render(request, template_name, context)

@login_required
@permission_required('inventory.can_generate_excel_report_count')
def generate_count_report(request):
	if request.method == 'POST':
		form = ReportFilterForm(request.POST)

		if form.is_valid():

			client = form.cleaned_data['client']

			today = datetime.today().strftime('%m-%d-%Y')

			wb = xlwt.Workbook(encoding='utf-8')

			excel = ExcelWriter()

			# base filter
			base_filter = Q(unit__business_unit__client=client) & Q(active=True) & Q(unit__active=True)

			# MACHINE COUNT SHEET

			sheet_name = 'Machine type count'
			columns = ['Machine type', 'Count',]
			machine_count = MachineType.objects.filter(base_filter)\
											  .annotate(machine_count=Count('unit'))
			machine_count = machine_count.values_list('machine_type_name', 'machine_count').order_by('-machine_count')
			
			excel.create_count_per_item(wb, sheet_name, columns, machine_count)

			# END MACHINE COUNT SHEET

			# PROCESSOR COUNT SHEET

			sheet_name = 'Processor count'
			columns = ['Processor', 'Count',]
			processor_count = Processor.objects.filter(base_filter)\
											  .annotate(processor_count=Count('unit'))
			processor_count = processor_count.values_list('processor_name', 'processor_count').order_by('-processor_count')
			
			excel.create_count_per_item(wb, sheet_name, columns, processor_count)

			# END PROCESSOR COUNT SHEET

			# TOTAL RAM COUNT SHEET

			sheet_name = 'Total ram count'
			columns = ['RAM', 'Count',]
			total_ram_count = TotalRam.objects.filter(base_filter)\
											  .annotate(total_ram_count=Count('unit'))
			total_ram_count = total_ram_count.values_list('total_ram_name', 'total_ram_count').order_by('-total_ram_count')
			
			excel.create_count_per_item(wb, sheet_name, columns, total_ram_count)

			# END TOTAL RAM COUNT SHEET

			# TOTAL RAM COUNT SHEET

			sheet_name = 'HDD count'
			columns = ['HDD', 'Count',]
			hdd_size_count = HddSize.objects.filter(base_filter)\
											  .annotate(hdd_size_count=Count('unit'))
			hdd_size_count = hdd_size_count.values_list('hdd_size_name', 'hdd_size_count').order_by('-hdd_size_count')
			
			excel.create_count_per_item(wb, sheet_name, columns, hdd_size_count)

			# END TOTAL RAM COUNT SHEET

			# MONITOR TYPE COUNT SHEET

			sheet_name = 'Monitor type count'
			columns = ['Monitor type', 'Count',]
			monitor_type_count = Unit.objects.filter(active=True, business_unit__client=client)\
	                                 .values('monitor_type')\
									 .order_by('monitor_type')\
									 .annotate(monitor_type_count=Count('monitor_type'))
			monitor_type_count = monitor_type_count.values_list('monitor_type', 'monitor_type_count').order_by('-monitor_type_count')
			
			excel.create_count_per_item(wb, sheet_name, columns, monitor_type_count)

			# END MONITOR TYPE COUNT SHEET

			# STATUS COUNT SHEET

			sheet_name = 'Status count'
			columns = ['Status', 'Count',]
			status_count = Unit.objects.filter(active=True, business_unit__client=client)\
	                                 .values('status')\
									 .order_by('status')\
									 .annotate(status_count=Count('status'))
			status_count = status_count.values_list('status', 'status_count').order_by('-status_count')
			
			excel.create_count_per_item(wb, sheet_name, columns, status_count)

			# END STATUS COUNT SHEET

			# BRAND COUNT SHEET

			sheet_name = 'Brand count'
			columns = ['Brand', 'Count',]
			brand_count = Unit.objects.filter(active=True, business_unit__client=client)\
	                          .values('machine_brand__brand_name')\
	                          .order_by('machine_brand__brand_name')\
	                          .annotate(brand_count=Count('machine_brand'))
			brand_count = brand_count.values_list('machine_brand__brand_name', 'brand_count').order_by('-brand_count')
			
			excel.create_count_per_item(wb, sheet_name, columns, brand_count)

			# END BRAND COUNT SHEET

			response = HttpResponse(content_type='application/ms-excel')
			response['Content-Disposition'] = 'attachment; filename="{0}_{1}-Count.xls"'.format(today, client)

			wb.save(response)
			return response
	else:
		form = ReportFilterForm()

	context = {'form':form}

	return render(request, 'report/report_main.html', context)

class CertificationFormView(LoginRequiredMixin, PermissionRequiredMixin, View):
	permission_required = 'inventory.can_generate_certification_form'
	login_url = settings.LOGOUT_REDIRECT_URL
	template_name = 'report/certification_form.html'

	def post(self, request, *args, **kwargs):

		form = CertficateFilterForm(request.POST)

		if form.is_valid():
			business_unit_id = request.POST['business_unit']
			return redirect('/inventory/generate-certification-form/' + business_unit_id + '/')

		context = {
			'form':form
		}
		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):

		form = CertficateFilterForm()

		context = {
			'form':form
		}
		return render(request, self.template_name, context)