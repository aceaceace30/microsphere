from django import forms
from .models import Unit, PreventiveMaintenance


class PrinterForm(forms.ModelForm):

    class Meta:
        model = Unit
        fields = ('business_unit', 'machine_type', 'machine_brand', 'model',
                  'serial_number', 'computer_tag', 'mst_tag', 'user', 'designation', 'remarks')
        #exclude = ('active','created_at', 'updated_at', 'created_by', 'updated_by')

class PcForm(forms.ModelForm):

    class Meta:
        model = Unit
        #fields = ('business_unit', 'model', 'serial_number', 'computer_tag', 'mst_tag', 'user', 'designation')
        exclude = ('active','created_at', 'updated_at', 'created_by', 'updated_by')

class UnitForm(forms.ModelForm):

    class Meta:
        model = Unit
        #fields = ()
        exclude = ('active','created_at', 'updated_at', 'created_by', 'updated_by')

class PreventiveMaintenanceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs): 
        super(PreventiveMaintenanceForm, self).__init__(*args, **kwargs)
        self.fields['service_report_number'].label = 'SR #'

    class Meta:
        model = PreventiveMaintenance
        #fields = ()
        exclude = ('status','active','created_at', 'updated_at', 'created_by', 'updated_by')