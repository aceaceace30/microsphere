from django import forms
from .models import Unit, PreventiveMaintenance, AREA, BusinessUnit, ClientProfile

class UnitForm(forms.ModelForm):

    client = forms.ModelChoiceField(queryset=ClientProfile.objects.filter(active=True), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['client'].initial = self.instance.business_unit.client
        except:
            pass
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = Unit
        exclude = ('active','created_at', 'updated_at', 'created_by', 'updated_by')

    field_order = ['client', 'area', 'business_unit', 'machine_type', 'machine_brand', 
                   'model', 'serial_number', 'computer_tag', 'mst_tag', 'working', 
                   'status', 'user', 'designation', 'operating_system', 'office_application', 
                   'host_name', 'mac_address', 'ip_address', 'processor', 'total_ram', 
                   'hdd_size', 'monitor_type', 'monitor_brand', 'monitor_size', 'remarks']


class PreventiveMaintenanceForm(forms.ModelForm):

    # add extra field for emails
    emails = forms.CharField(widget=forms.Textarea(), required=False)

    date_format = 'mm/dd/yyyy'
    time_format = 'hh:mm'

    def __init__(self, *args, **kwargs): 
        super(PreventiveMaintenanceForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-sm'
        #self.fields['service_report_number'].label = 'SR #'
        self.fields['target_date'].widget.attrs['placeholder'] = self.date_format
        self.fields['target_time'].widget.attrs['placeholder'] = self.time_format
        self.fields['actual_date'].widget.attrs['placeholder'] = self.date_format

    class Meta:
        model = PreventiveMaintenance
        exclude = ('service_report_number', 'pm_done', 'pm_date_done', 'active','created_at', 'updated_at', 'created_by', 'updated_by')

class PreventiveMaintenanceEditForm(forms.ModelForm):

    date_format = 'mm/dd/yyyy'
    time_format = 'hh:mm'

    def __init__(self, *args, **kwargs): 
        super(PreventiveMaintenanceEditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-sm'
        #self.fields['service_report_number'].label = 'SR #'
        self.fields['target_date'].widget.attrs['placeholder'] = self.date_format
        self.fields['target_time'].widget.attrs['placeholder'] = self.time_format
        self.fields['actual_date'].widget.attrs['placeholder'] = self.date_format

    class Meta:
        model = PreventiveMaintenance
        exclude = ('service_report_number', 'pm_done', 'pm_date_done',
                   'active','created_at', 'updated_at', 'created_by', 'updated_by')