import re
from django.core.exceptions import ValidationError
import os

def validate_mac_address(value):

	if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", value.lower()):
		return value
	else:
		raise ValidationError('Enter a valid mac address.')

def validate_file_extension(value):
    
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf',]
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')