from django import forms
from .models import Unit, PreventiveMaintenance, AREA, BusinessUnit, ClientProfile, PmUnitHistory

# bootstrap datepicker
# from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput

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

        self.fields['target_date'].widget.attrs['placeholder'] = self.date_format
        self.fields['target_time'].widget.attrs['placeholder'] = self.time_format

    class Meta:
        model = PreventiveMaintenance
        exclude = ('service_report_number', 'pm_done', 'pm_date_done', 'attachment',
                   'active','created_at', 'updated_at', 'created_by', 'updated_by')

        # widgets = {
        #         'target_date': DatePickerInput(),
        #         'target_time': TimePickerInput(),
        # }

class PreventiveMaintenanceEditForm(forms.ModelForm):

    date_format = 'mm/dd/yyyy'
    time_format = 'hh:mm'

    def __init__(self, *args, **kwargs): 
        super(PreventiveMaintenanceEditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-sm'

        self.fields['target_date'].widget.attrs['placeholder'] = self.date_format
        self.fields['target_time'].widget.attrs['placeholder'] = self.time_format

    class Meta:
        model = PreventiveMaintenance
        exclude = ('service_report_number', 'pm_done', 'pm_date_done', 'attachment',
                   'active','created_at', 'updated_at', 'created_by', 'updated_by')

        # widgets = {
        #         'target_date': DatePickerInput(),
        #         'target_time': TimePickerInput(),
        # }

class NotesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NotesForm, self).__init__(*args, **kwargs)

        self.fields['remarks'].widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = PmUnitHistory

        fields = ('remarks',)

class ServiceReportForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ServiceReportForm, self).__init__(*args, **kwargs)
        self.fields['service_report_number'].required = False
        self.fields['service_report_number'].widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = PreventiveMaintenance

        fields = ('service_report_number',)

class UploadAttachmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UploadAttachmentForm, self).__init__(*args, **kwargs)
        #self.fields['attachment'].widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = PreventiveMaintenance

        fields = ('attachment',)