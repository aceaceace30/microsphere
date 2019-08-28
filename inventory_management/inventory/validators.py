import re
from django.core.exceptions import ValidationError

def validate_mac_address(value):

	if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", value.lower()):
		return value
	else:
		raise ValidationError('Enter a valid mac address.')