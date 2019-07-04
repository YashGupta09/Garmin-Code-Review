from django.core.files import File
from django.conf import settings

with open(settings.CONFIG_FILE_PATH, 'r') as f:
	config_data = File(f).read()

def write_config(config_data):
	with open(settings.CONFIG_FILE_PATH, 'w') as f:
		File(f).write(config_data)