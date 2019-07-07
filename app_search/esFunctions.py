from elasticsearch import Elasticsearch
from .populate import printOnTerminal
import requests

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

response = requests.get('http://localhost:9200')

def delFromEs(oldDocCount):
	printOnTerminal("deleting old documents from garmin_index")
	for i in range(oldDocCount):
		es.delete(index="garmin_index", doc_type="files", id=(i+1))
	printOnTerminal(str(oldDocCount) + " old documents deleted")

def addToEs(files):
	oldDocCount = es.search(index="garmin_index", size=10000, body={})["hits"]["total"]["value"]
	delFromEs(oldDocCount)
	printOnTerminal("adding documents to garmin_index")
	newDocCount = 0
	for file in files:
		es.index(index="garmin_index", doc_type="files", id=file['id'], body=file)
		newDocCount+=1
	printOnTerminal(str(newDocCount) + " documents added to garmin_index")

def mySearch(attribute1=None, value1=None, attribute2=None, value2=None):
	resultList = []
	contentFlag = False
	#conditions the check the number of arguments
	if attribute1 == None and value1 == None and attribute2 == None and value2 == None:
		search_result = es.search(index="garmin_index", size=10000, body={})
	elif attribute2 == None and value2 == None:
		if attribute1 != "content":
			search_result = es.search(index="garmin_index", size=10000, body={"query": {"regexp": {attribute1: value1}}})
		else:
			search_result = es.search(index="garmin_index", size=10000, body={"query": {"regexp": {attribute1: value1}}, "highlight": {"fields": {"content": {}}}})
			contentFlag = True
	else:
		search_result = es.search(index="garmin_index", size=10000, body={"query": {"bool": {"must": [{"regexp": {attribute1: value1}}, {"regexp": {attribute2: value2}}]}}, "highlight": {"fields": {"content": {}}}})
		contentFlag = True
	#retrieve data and return it
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