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
		fileTuple[0]['highlight'] = []
		for outList in contentList:
			for inList in outList:
				fileTuple[0]['highlight'].append(inList)
		newFiles.append(fileTuple[0])
	printOnTerminal("Number of files in search result is " + str(len(files)))
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

def view_file(request, doc_id, argu):
	contentList = esFunctions.myIdSearch(doc_id)['_source']['content'].split('\n')
	lineList = []
	regex = re.compile(argu, re.IGNORECASE)
	i = 0

	for line in contentList:
		i += 1
		if regex.search(line) != None:
			lineList.append(i)
	print("Line number are " + str(lineList))
	return render(request, 'app_search/view_file.html', {'title': 'File View'})