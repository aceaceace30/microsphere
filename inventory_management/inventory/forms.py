from django import forms
from .models import Unit, PreventiveMaintenance


class UnitForm(forms.ModelForm):
    """
    Render the basic crud create form
    
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter your full name',
                                      'maxlength': '75'}))

    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter your working email',
                                      'maxlength': '254'}))

    subject = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Enter your subject',
            'maxlength': '75'}))

    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control textarea',
                                     'placeholder': 'Enter your message'}))
    """

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