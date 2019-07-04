from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from . import esFunctions
from .populate import populate as popFunc, printOnTerminal
from .forms import SearchForm
import re

# Create your views here
def populate(request):
    popFunc()
    messages.success(request, f'Database populated.')
    return redirect('app_search')

def search(request):
	form = SearchForm()
	return render(request, 'app_search/search.html', {'form': form})

def api(request):
	fileName = request.GET.get('fileName')
	content = request.GET.get('content')
	fileNameRegEx = ".*" + fileName + ".*"
	contentRegEx = ".*" + content + ".*"

	if fileName:
		if content:
			files = esFunctions.mySearch(
				"fileName", fileNameRegEx, "content", contentRegEx)
		else:
			files = esFunctions.mySearch("fileName", fileNameRegEx)
	elif content:
		files = esFunctions.mySearch("content", contentRegEx)
	else:
		files = esFunctions.mySearch()

	for file in files:
		printOnTerminal(file['fileName'])
	return JsonResponse(files, safe=False)

def lineNums(request):
	doc_id = int(request.POST.get('doc_id'))
	argu = request.POST.get('argu')

	file_content = esFunctions.mySearch("id", doc_id)[0]['content']

	lineNums = list()
	regex = re.compile(argu, re.IGNORECASE)
	i = 0
	for line in file_content:
		i += 1
		if regex.search(line) != None:
			lineNums.append(i)	
	return JsonResponse(lineNums, safe=False)