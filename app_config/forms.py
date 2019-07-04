from django import forms
from .read_config import config_data

class ConfigForm(forms.Form):
	config_file = forms.CharField(widget=forms.Textarea(attrs={'rows':35, 'spellcheck':'false'}), initial=config_data, label='File')