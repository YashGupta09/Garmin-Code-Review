from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ConfigForm
from .read_config import write_config

# Create your views here.
def config(request):
	if request.method == 'POST':
		form = ConfigForm(request.POST)
		if form.is_valid():
			new_config_data = form.cleaned_data.get('config_file')
			write_config(new_config_data.replace('\r', ''))
			messages.success(request, f'Configs are saved.')
			return redirect('app_search')
	else:
		form = ConfigForm()
	return render(request, 'app_config/config.html', {'form': form, 'title': 'Config'})