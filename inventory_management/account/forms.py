from django import forms
from inventory.models import BusinessUnit, ClientProfile

class DashboardFilterForm(forms.Form):

	client = forms.ModelChoiceField(queryset=ClientProfile.objects.none(), required=False)
	business_unit = forms.ModelChoiceField(queryset=BusinessUnit.objects.none(), required=False)

	def __init__(self, client, *args, **kwargs):
		super(DashboardFilterForm, self).__init__(*args, **kwargs)
		self.fields['client'].queryset = ClientProfile.objects.filter(pk=client.pk) if client else ClientProfile.objects.filter(active=True)
		self.fields['business_unit'].queryset = BusinessUnit.objects.filter(active=True, client=client) if client else BusinessUnit.objects.filter(active=True)
		
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control form-control-sm'