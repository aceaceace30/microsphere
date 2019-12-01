from django import forms
from inventory.models import AREA, ClientProfile, BusinessUnit

class ReportFilterForm(forms.Form):

	# REPORT_TYPE = (
	# 	('Machine Type', 'Machine Type'),
	# 	('Processor', 'Processor'),
	# 	('Total Ram', 'Total Ram'),
	# 	('HDD Size', 'HDD Size'),
	# 	('Monitor Type', 'Monitor Type'),
	# 	('Status', 'Status'),
	# 	)

	# report_type = forms.ChoiceField(choices=REPORT_TYPE)
	client = forms.ModelChoiceField(queryset=ClientProfile.objects.filter(active=True))
	
	def __init__(self, *args, **kwargs):
		super(ReportFilterForm, self).__init__(*args, **kwargs)

		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control form-control-sm'