from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from . import esFunctions
from .populate import populate as popFunc, printOnTerminal
from .forms import SearchForm
import re

def convergeDict(files):
	# Helper function
	def extractLines(highlight):
		highlightList = highlight.split('\n')
		newHighlightList = []
		for line in highlightList:
			if line.find('<em>') != -1:
				newHighlightList.append(line.replace('<em>', '').replace('</em>', ''))
		return newHighlightList

	# Function body begins here
	newFiles = []
	for fileTuple in files:
		contentList = []
		for content in fileTuple[1]['content']: 
			contentList.append(extractLines(content))
		fileTuple[0]['highlight'] = contentList
		newFiles.append(fileTuple[0])
	for files in newFiles:
		print(files['highlight'])
	return newFiles

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
	contentFlag = False

	if fileName:
		if content:
			files = esFunctions.mySearch("fileName", fileNameRegEx, "content", contentRegEx)
			contentFlag = True
		else:
			files = esFunctions.mySearch("fileName", fileNameRegEx)
	elif content:
		files = esFunctions.mySearch("content", contentRegEx)
		contentFlag = True
	else:
		files = esFunctions.mySearch()

	if contentFlag:
		files = convergeDict(files)
	return JsonResponse(files, safe=False)

def lineNums(request):
	doc_id = int(request.GET.get('doc_id'))
	argu = request.GET.get('argu')

	contentList = esFunctions.myIdSearch(doc_id)['_source']['content'].split('\n')
	lineDict = {}
	lineDict['numbers'] = []
	regex = re.compile(argu, re.IGNORECASE)
	i = 0

	for line in contentList:
		i += 1
		if regex.search(line) != None:
			lineDict['numbers'].append(i)
	return JsonResponse(lineDict)