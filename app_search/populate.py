from django.core.files import File as DjangoFile
from django.conf import settings
from .config import paths as rootPaths, ext
from . import esFunctions
import os

def printOnTerminal(fileName, message):
    print ("[" + str(fileName) + ".py]-- " + message + " --")

def writeToRootData(rootDict):
    root_data = "root_data = {"
    for root in rootDict:
        root_data += "r'" + root + "': [" + str(rootDict[root][0]) + ", " + str(rootDict[root][1]) + "], "
    root_data += "}"
    with open(settings.ROOTDATA_FILE_PATH, 'w') as f:
        DjangoFile(f).write(root_data)

def populate():
    printOnTerminal("app_search/populate", "populate.py called")

    rootDict = {}
    fileList = []
    prevRoot = None
    count = 1

    for rootPath in rootPaths:
        #collecting data for rootData.py
        if prevRoot != None:
            rootDict[prevRoot].append(count-1)
        rootDict[rootPath] = []
        rootDict[rootPath].append(count)
        prevRoot = rootPath
        #actual populate function starts here
        for root, directories, files in os.walk(rootPath):
            for file in files:
                #fileComp stores the components of file, ie, filename and extention
                fileComp = os.path.splitext(file)
                if fileComp[1] in ext:
                    filePath = root + '/' + file
                    with open(filePath, mode='r', encoding='utf8') as f:
                        content = DjangoFile(f).read()
                    #creating new File object for every file
                    fileList.append({'id': count, 'root': root, 'fileName': file, 'content': content})
                    printOnTerminal("app_search/populate", "reading " + filePath)        
                    count += 1
    rootDict[prevRoot].append(count-1)
        
    printOnTerminal("app_search/populate", str(count-1) + " files found in the root path(s)")

    esFunctions.addToEs(fileList)

    writeToRootData(rootDict)