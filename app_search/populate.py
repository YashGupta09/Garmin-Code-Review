from .config import paths as rootPaths, ext
from django.core.files import File as DjangoFile
from . import esFunctions
import os

def printOnTerminal(fileName, message):
    print ("[" + str(fileName) + ".py]-- " + message + " --")

def populate():
    printOnTerminal("app_search/populate", "populate.py called")

    fileList = []
    count = 0

    for rootPath in rootPaths:
        for root, directories, files in os.walk(rootPath):
            for file in files:
                #fileComp stores the components of file, ie, filename and extention
                fileComp = os.path.splitext(file)
                if fileComp[1] in ext:
                    filePath = root + '\\' + file
                    with open(filePath, mode='r', encoding='utf8') as f:
                        content = DjangoFile(f).read()
                    
                    #creating new File object for every file
                    fileList.append({'id': count+1, 'root': root, 'fileName': file, 'content': content})
                    printOnTerminal("app_search/populate", "reading " + filePath)        
                    count += 1
        
    printOnTerminal("app_search/populate", str(count) + " files found in the root path(s)")

    esFunctions.addToEs(fileList)