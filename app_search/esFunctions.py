from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from .rootData import root_data
from .populate import printOnTerminal
import requests

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

response = requests.get('http://localhost:9200')

def delFromEs(oldDocCount):
	# generator function
	def genDelData(count):
		for i in range(count):
			yield {
				"_op_type": "delete",
				"_index": "garmin_index",
				"_type": "files",
				"_id": i+1
			}

	printOnTerminal("app_search/esFunctions", "deleting old documents from garmin_index")
	bulk(es, genDelData(oldDocCount))
	printOnTerminal("app_search/esFunctions", str(oldDocCount) + " old documents deleted")

def addToEs(files):
	# generator function
	def genAddData(files):
		for file in files:
			yield {
				"_index": "garmin_index",
				"_type": "files",
				"_id": file["id"],
				"_source": {
					"id": file["id"],
					"root": file["root"],
					"fileName": file["fileName"],
					"content": file["content"]
				}
			}

	try:
		oldDocCount = es.search(index="garmin_index", size=10000, body={})["hits"]["total"]["value"]	
		delFromEs(oldDocCount)
	except:
		printOnTerminal("app_search/esFunctions", "garmin_index not found")
	finally:
		printOnTerminal("app_search/esFunctions", "adding documents to garmin_index")
		bulk(es, genAddData(files))
		printOnTerminal("app_search/esFunctions", str(len(files)) + " documents added to garmin_index")

def mySearch(notRootPaths, attribute1=None, value1=None, attribute2=None, value2=None):
	# helper function
	def buildRootQuery():
		pathCount = 0
		if not notRootPaths:
			query = '{"query": {"bool": {"must_not": []'
		else:
			query = '{"query": {"bool": {"must_not": ['
			for path in notRootPaths:
				pathCount += 1
				if pathCount != len(notRootPaths):
					query += '{"range": {"id": {"gte": ' + str(root_data[path][0]) + ', "lte": ' + str(root_data[path][1]) + '}}}, '
				else:
					query += '{"range": {"id": {"gte": ' + str(root_data[path][0]) + ', "lte": ' + str(root_data[path][1]) + '}}}]'
		return query
	
	# helper function
	def buildContentQuery(query, arguString):
		argus = arguString.split(' ')
		arguCount = 0
		query += ', "should": ['
		for argu in argus:
			arguCount += 1
			if arguCount != len(argus):
				query += '{"regexp": {"content": ".*' + argu.lower() + '.*"}}, '
			else:
				query += '{"regexp": {"content": ".*' + argu.lower() + '.*"}}]'
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
	printOnTerminal("app_search/esFunctions", "ES Query > " + query)
	search_result = es.search(index="garmin_index", size=10000, body=query)
	printOnTerminal("app_search/esFunctions", str(len(search_result['hits']['hits'])) + " results found")
	# retrieve data and return it
	if contentFlag:
		for hits in search_result['hits']['hits']:
			try:
				resultList.append((hits['_source'], hits['highlight']))
			except: continue
	else:
		for hits in search_result['hits']['hits']:
			resultList.append(hits['_source'])
	return resultList

def myIdSearch(doc_id):
	search_result = es.search(index="garmin_index", body={"query": {"ids": {"values": [doc_id]}}})
	return search_result['hits']['hits'][0]