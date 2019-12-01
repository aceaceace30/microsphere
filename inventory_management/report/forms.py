from django import forms
from inventory.models import BusinessUnit, ClientProfile, AREA

class CertficateFilterForm(forms.Form):

	client = forms.ModelChoiceField(queryset=ClientProfile.objects.filter(active=True), required=True)
	area = forms.ChoiceField(choices=AREA, required=True)
	business_unit = forms.ModelChoiceField(queryset=BusinessUnit.objects.filter(active=True), required=True)

	def __init__(self, *args, **kwargs):
		super(CertficateFilterForm, self).__init__(*args, **kwargs)
		
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control form-control-sm'


class ReportFilterForm(forms.Form):

	client = forms.ModelChoiceField(queryset=ClientProfile.objects.filter(active=True))
	
	def __init__(self, *args, **kwargs):
		super(ReportFilterForm, self).__init__(*args, **kwargs)

		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control form-control-sm'