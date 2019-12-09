from django.shortcuts import render, get_object_or_404

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings

from django.contrib.auth.models import Permission

from .models import Unit, PreventiveMaintenance, ClientProfile, BusinessUnit, Brand, Model
from django.db.models import Count, Q

from django.contrib.auth.decorators import login_required

from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

"""
DYNAMIC FILTERING
"""

@login_required
def load_business_units(request):
    client = request.GET.get('client')
    area = request.GET.get('area')
    business_unit_id = request.GET.get('business_unit')

    business_units = None

    filter_ = Q(active=True)

    if client:
        filter_ &= Q(client=client)
    if area:
        filter_ &= Q(area=area)
        business_units = BusinessUnit.objects.filter(filter_)

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
                (SELECT DISTINCT brand_id FROM inventory_model WHERE machine_type_id={0} and active=true) AS model\
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


"""
XHTML2PDF
"""
def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

"""
XHTML2PDF
"""
class Render:
    @staticmethod
    def render(path: str, filename: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response, link_callback=link_callback)

        if not pdf.err:
            response = HttpResponse(response.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="{0}.pdf"'.format(filename)
            return response
        else:
            return HttpResponse("Error Rendering PDF", status=400)

def check_perm(self, perm):
    user = self.request.user
    # check user if has permission
    if not user.is_superuser:
        perms = Permission.objects.filter(Q(user=user) | Q(group__user=user)).distinct()
        return perms.filter(codename=perm).exists()
    return True

"""
DATA TABLE SERVER SIDE PROCESSING
"""
class UnitListJson(BaseDatatableView):
    # The model we're going to show
    model = Unit

    # define the columns that will be returned
    columns = ['serial_number', 'client', 'area', 'business_unit', 'location', 'status']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['serial_number', 'business_unit__client', 'area', 'business_unit', 'business_unit__location', 'status']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 1000

    def get_initial_queryset(self):
        self.can_view_unit = check_perm(self, 'view_unit')
        return Unit.get_active_units(self.request)

    def render_column(self, row, column):
        if column == 'serial_number':

            machine_class = row.machine_type.machine_class.upper()
            
            if machine_class == 'CPU':
                img = 'CPU_ICON.ico'
                alt = 'CPU Icon'
            elif machine_class == 'LAPTOP':
                img = 'LAPTOP_ICON.ico'
                alt = 'LAPTOP Icon'
            elif machine_class == 'PRINTER':
                img = 'PRINTER_ICON.ico'
                alt = 'PRINTER Icon'

            img_display = '<img src="/static/inventory/images/{0}/" alt="{1}">'.format(img, alt)

            # check if has permission
            if self.can_view_unit:
                serial_number_row = '{0} <a href="/inventory/unit-view/{1}">{2}</a>'.format(img_display, row.pk, row.serial_number)
            else:
                serial_number_row = '{0} {1}'.format(img_display, row.serial_number)

            return serial_number_row

        if column == 'client':
            # escape HTML for security reasons
            return escape('{0}'.format(row.business_unit.client.client_code))
        if column == 'area':
            # escape HTML for security reasons
            return escape('{0}'.format(row.area))
        if column == 'business_unit':
            # escape HTML for security reasons
            return escape('{0}'.format(row.business_unit.business_unit_name))
        elif column == 'location':
            return escape('{0}'.format(row.business_unit.location))
        elif column == 'status':
            return escape('{0}'.format(row.status))
        else:
            return super(UnitListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        search = self.request.GET.get('search[value]', None)
        if search:
            filter_ = Q(business_unit__client__client_code__istartswith=search)
            filter_ |= Q(area__istartswith=search)
            filter_ |= Q(business_unit__business_unit_name__istartswith=search)
            filter_ |= Q(business_unit__location__istartswith=search)
            filter_ |= Q(serial_number__istartswith=search)
            filter_ |= Q(status__istartswith=search)
            qs = qs.filter(filter_)

        # more advanced example using extra parameters
        filter_serial_number = self.request.GET.get('columns[0][search][value]', None)
        if filter_serial_number:
            qs = qs.filter(serial_number__istartswith=filter_serial_number)

        filter_client = self.request.GET.get('columns[1][search][value]', None)
        if filter_client:
            qs = qs.filter(business_unit__client__client_code__istartswith=filter_client)

        filter_area = self.request.GET.get('columns[2][search][value]', None)
        if filter_area:
            qs = qs.filter(area__istartswith=filter_area)

        filter_business_unit = self.request.GET.get('columns[3][search][value]', None)
        if filter_business_unit:
            qs = qs.filter(business_unit__business_unit_name__istartswith=filter_business_unit)

        filter_location = self.request.GET.get('columns[4][search][value]', None)
        if filter_location:
            qs = qs.filter(business_unit__location__istartswith=filter_location)

        filter_status = self.request.GET.get('columns[5][search][value]', None)
        if filter_status:
            qs = qs.filter(status__istartswith=filter_status)

        return qs

class PmListJson(BaseDatatableView):
    # The model we're going to show
    model = PreventiveMaintenance

    # define the columns that will be returned
    columns = ['service_report_number', 'client', 'area', 'business_unit', 'target_date', 'pm_done']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['service_report_number', 'business_unit__client__client_code', 'business_unit__area', 'business_unit', 'target_date', 'pm_done']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 1000

    def get_initial_queryset(self):
        self.view_pm = check_perm(self, 'view_preventivemaintenance')
        status = self.request.GET.get('status', default=None)

        params = dict()

        if status:
            params['status'] = status

        if ClientProfile.objects.filter(username=self.request.user).exists():
            params['client'] = self.request.user.clientprofile

        return PreventiveMaintenance.get_active_pms(**params)

    def render_column(self, row, column):

        # check if has permission
        if self.view_pm:
            service_report_row = '<a href="/inventory/pm-view/{0}">{1}</a>'.format(row.pk, row.service_report_number)
        else:
            service_report_row = '{0}'.format(row.service_report_number)

        if column == 'service_report_number':
            return service_report_row
        elif column == 'client':
            # escape HTML for security reasons
            return escape('{0}'.format(row.business_unit.client.client_code))
        elif column == 'area':
            return escape('{0}'.format(row.business_unit.area))
        elif column == 'business_unit':
            return escape('{0}'.format(row.business_unit.business_unit_name))
        elif column == 'target_date':
            return escape('{0}'.format(row.target_date.strftime('%B %d, %Y')))
        elif column == 'pm_done':
            if row.pm_done:
                display = '<span class="badge badge-pill badge-success">Done</span>'
            else:
                display = '<span class="badge badge-pill badge-danger">Pending</span>'
            return '{0}'.format(display)
        else:
            return super(PmListJson, self).render_column(row, column)

    def filter_queryset(self, qs):

        search = self.request.GET.get('search[value]', None)
        if search:
            filter_ = Q(service_report_number__istartswith=search)
            filter_ |= Q(business_unit__client__client_code__istartswith=search)
            filter_ |= Q(business_unit__area__istartswith=search)
            filter_ |= Q(business_unit__business_unit_name__istartswith=search)
            filter_ |= Q(target_date__istartswith=search)
            qs = qs.filter(filter_)

        # more advanced example using extra parameters
        filter_service_report_number = self.request.GET.get('columns[0][search][value]', None)
        if filter_service_report_number:
            qs = qs.filter(service_report_number__istartswith=filter_service_report_number)

        filter_client = self.request.GET.get('columns[1][search][value]', None)
        if filter_client:
            qs = qs.filter(business_unit__client__client_code__istartswith=filter_client)

        filter_area = self.request.GET.get('columns[2][search][value]', None)
        if filter_area:
            qs = qs.filter(business_unit__area__istartswith=filter_area)

        filter_business_unit = self.request.GET.get('columns[3][search][value]', None)
        if filter_business_unit:
            qs = qs.filter(business_unit__business_unit_name__istartswith=filter_business_unit)

        filter_target_date = self.request.GET.get('columns[4][search][value]', None)
        if  filter_target_date:
            qs = qs.filter(target_date__istartswith=filter_target_date)

        return qs