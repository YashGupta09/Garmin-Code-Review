from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from . import esFunctions
from .config import paths as rootPaths
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

	# convergeDict() body begins here
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
	printOnTerminal("app_search/views", "Number of files in search result is " + str(len(files)))
	return newFiles

# Create your views here
def populate(request):
    popFunc()
    messages.success(request, f'Database populated.')
    return redirect('app_search')

def search(request):
	form = SearchForm()
	return render(request, 'app_search/search.html', {'title': 'Garmin File Search', 'form': form, 'rootPaths': rootPaths})

def api(request):
	fileName = request.GET.get('fileName')
	content = request.GET.get('content')
	notRootPaths = request.GET.getlist('notRootPaths[]')
	fileNameRegEx = ".*" + fileName + ".*"
	contentFlag = False

	if fileName:
		if content:
			files = esFunctions.mySearch(notRootPaths, "fileName", fileNameRegEx, "content", content)
			contentFlag = True
		else:
			files = esFunctions.mySearch(notRootPaths, "fileName", fileNameRegEx)
	elif content:
		files = esFunctions.mySearch(notRootPaths, "content", content)
		contentFlag = True
	else:
		files = esFunctions.mySearch(notRootPaths)

	if contentFlag:
		files = convergeDict(files)
	return JsonResponse(files, safe=False)

def view_file_argu(request, doc_id, arguString):
	search_result = esFunctions.myIdSearch(doc_id)['_source']
	fileFullPath = search_result['root'] + "\\" + search_result['fileName']
	contentList = search_result['content'].split('\n')
	content = []
	i = 0
	
	regexes = []
	argus = arguString.split(' ')
	for argu in argus:
		regexes.append(re.compile(argu, re.IGNORECASE))

	for line in contentList:
		i += 1
		highlightFlag = False
		for regex in regexes:
			if regex.search(line) != None:
				content.append({'lineNum': i, 'lineContent': r"<span style='background-color: #98FB98;'>" + ("%r"%line)[1:-1] + r"</span>"})
				highlightFlag = True
				break
		if not highlightFlag: content.append({'lineNum': i, 'lineContent': line})
		else: continue
		
	return render(request, 'app_search/view_file.html', {'title': 'Garmin File Search - ' + search_result['fileName'], 'fullFilePath': fileFullPath , 'content': content})

def view_file(request, doc_id):
	search_result = esFunctions.myIdSearch(doc_id)['_source']
	fileFullPath = search_result['root'] + "\\" + search_result['fileName']
	contentList = search_result['content'].split('\n')
	content = []
	i = 0
	
	for line in contentList:
		i += 1
		content.append({'lineNum': i, 'lineContent': line})
		
	return render(request, 'app_search/view_file.html', {'title': 'Garmin FIle Search - ' + search_result['fileName'], 'fullFilePath': fileFullPath , 'content': content})