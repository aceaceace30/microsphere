from django import forms
from inventory.models import BusinessUnit, ClientProfile, AREA

class DashboardFilterForm(forms.Form):

	AREA.insert(0, ('', '--------'))

	client = forms.ModelChoiceField(queryset=ClientProfile.objects.none(), required=False)
	area = forms.ChoiceField(choices=AREA, required=False)
	business_unit = forms.ModelChoiceField(queryset=BusinessUnit.objects.none(), required=False)

	def __init__(self, client, *args, **kwargs):
		super(DashboardFilterForm, self).__init__(*args, **kwargs)

		self.fields['client'].queryset = ClientProfile.objects.filter(pk=client.pk)\
		if client else ClientProfile.objects.filter(active=True)

		self.fields['business_unit'].queryset = BusinessUnit.objects.filter(active=True, client=client)\
		if client else BusinessUnit.objects.filter(active=True)

		if client:
			self.fields['client'].empty_label = None
		
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control form-control-sm'
	