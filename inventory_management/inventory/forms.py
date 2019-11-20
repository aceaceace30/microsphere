from django import forms
from .models import Unit, PreventiveMaintenance, AREA, BusinessUnit

class UnitForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = Unit
        exclude = ('active','created_at', 'updated_at', 'created_by', 'updated_by')


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
        exclude = ('service_report_number', 'pm_done', 'pm_date_done', 'active','created_at', 'updated_at', 'created_by', 'updated_by')