from elasticsearch import Elasticsearch
from .rootData import root_data
from .populate import printOnTerminal
import requests

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

response = requests.get('http://localhost:9200')

def delFromEs(oldDocCount):
	printOnTerminal("app_search/esFunctions", "deleting old documents from garmin_index")
	for i in range(oldDocCount):
		es.delete(index="garmin_index", doc_type="files", id=(i+1))
	printOnTerminal("app_search/esFunctions", str(oldDocCount) + " old documents deleted")

def addToEs(files):
	# oldDocCount = es.search(index="garmin_index", size=10000, body={})["hits"]["total"]["value"]
	# delFromEs(oldDocCount)
	printOnTerminal("app_search/esFunctions", "adding documents to garmin_index")
	newDocCount = 0
	for file in files:
		es.index(index="garmin_index", doc_type="files", id=file['id'], body=file)
		newDocCount+=1
	printOnTerminal("app_search/esFunctions", str(newDocCount) + " documents added to garmin_index")

def mySearch(notRootPaths, attribute1=None, value1=None, attribute2=None, value2=None):
	# helper functions
	def buildRootQuery():
		pathCount = 0
		n = len(notRootPaths)
		if not notRootPaths:
			query = '{"query": {"bool": {"must_not": []'
		else:
			query = '{"query": {"bool": {"must_not": ['
			for path in notRootPaths:
				pathCount += 1
				if pathCount != n:
					query += '{"range": {"id": {"gte": ' + str(root_data[path][0]) + ', "lte": ' + str(root_data[path][1]) + '}}}, '
				else:
					query += '{"range": {"id": {"gte": ' + str(root_data[path][0]) + ', "lte": ' + str(root_data[path][1]) + '}}}]'
		return query
	
	def buildContentQuery(query, arguString):
		argus = arguString.split(' ')
		arguCount = 0
		n = len(argus)
		query += ', "should": ['
		for argu in argus:
			arguCount += 1
			if arguCount != n:
				query += '{"regexp": {"content": ".*' + argu + '.*"}}, '
			else:
				query += '{"regexp": {"content": ".*' + argu + '.*"}}]'
		return query

	# mySearch() body begins here
	resultList = []
	contentFlag = False
	# building norRootPath part of the query, it's same for every combination of arguments
	query = buildRootQuery()
	# conditions to check the number of arguments
	if attribute1 == None and value1 == None and attribute2 == None and value2 == None:
		query += '}}}'
	elif attribute2 == None and value2 == None:
		if attribute1 != "content":
			query += ', "must": {"regexp": {"' + attribute1 + '": "' + value1 + '"}}}}}'
		else:
			query = buildContentQuery(query, value1)
			query += '}}, "highlight": {"fields": {"content": {}}}}'
			contentFlag = True
	else:
		query = buildContentQuery(query, value2)
		query += ', "must": {"regexp": {"' + attribute1 + '": "' + value1 + '"}}}}, "highlight": {"fields": {"content": {}}}}'
		contentFlag = True
	printOnTerminal("esFunctions", "ES Query > " + query)
	search_result = es.search(index="garmin_index", size=10000, body=query)
	# retrieve data and return it
	if contentFlag:
		for hits in search_result['hits']['hits']:
			resultList.append((hits['_source'], hits['highlight']))
	else:
		for hits in search_result['hits']['hits']:
			resultList.append(hits['_source'])
	return resultList

def myIdSearch(doc_id):
	search_result = es.search(index="garmin_index", body={"query": {"ids": {"values": [doc_id]}}})
	return search_result['hits']['hits'][0]