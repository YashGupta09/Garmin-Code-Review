from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Context, Template
from app_cmp.forms import SearchForms
from app_cmp.models import FileTable, PathTable
from django_tables2 import RequestConfig
from django.db.models import Q

from app_cmp.models import TempTable

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

import app_cmp.word_finder as getData
import app_cmp.searchInFiles as searchKeyWord
import app_cmp.populate as pop

# Create your views here.


def index(request):
    form = SearchForms()
    return render(request, 'app_cmp/index.1.html', {'form': form})

# Function to search and return file Names in DB based on Search String


def getDataBasedOnFileName(table):
    def insertDB(_list):
        import django
        django.setup()
        TempTable.objects.all().delete()

        for i in _list:
            c = TempTable.objects.get_or_create(SearchTerm=i[0], RootPath=i[1],
                                                FileName=i[2], lineNumber=i[3], CodeLine=i[4])[0]
            c.save()

    def initial_letter_filter(text, line,  autoescape=True):
        result = "<a href=\"displayFile/" + \
            str(text) + "\">" + str(line) + "</a>"
        return mark_safe(result)

    i = []
    a = []
    for x in table:
        for _i in table[x]:
            a.append(x)
            for c in _i:
                a.append(c)
            i.append(a)
            a = []
    insertDB(i)

    table = TempTable.objects.all()

    i = []
    a = []
    for x in table:
        a.append(x.SearchTerm)
        a.append(x.RootPath)
        a.append(x.FileName)
        a.append(initial_letter_filter(x.FileID, x.lineNumber))
        a.append(initial_letter_filter(x.FileID, x.CodeLine))
        i.append(a)
        a = []

    return i

# Returns list of file page


def fileList(request):

    form = SearchForms()
    if request.method == "POST":
        form = SearchForms(request.POST)
        data = request.POST.get('search')
        args = request.POST.get('search1')
        args = list(args.strip().split())
        print(data)
        print(args)
        if len(args) < 1 and len(str(data)) < 1:
            pass

        elif len(args) < 1:
            table = FileTable.objects.filter(Q(FileName__contains=str(data)))

            def initial_letter_filter(text, autoescape=True):
                result = "<a href=\"displayFilePlain/" + \
                    str(text) + "\">Visit File</a>"
                return mark_safe(result)

            i = []
            a = []
            for x in table:
                a.append(x.RootPath)
                a.append(x.FileName)
                a.append(x.Extension)
                a.append(initial_letter_filter(x.FileID))
                i.append(a)
                a = []
            return render(request, 'app_cmp/fileList.html', {'files': i})

        elif len(args) > 0 and len(data.strip()) > 0:
            table = FileTable.objects.filter(Q(FileName__contains=str(data)))
            i = []
            for x in table:
                print(str(x.RootPath) + "\\" + str(x.FileName))
                i.append(str(x.RootPath) + "\\" + str(x.FileName))

            table = searchKeyWord.searchInFiles(args, i).getValues()
            i = getDataBasedOnFileName(table)

            return render(request, 'app_cmp/fileList.1.html', {'files': i})

        else:
            table = getData.getResult(args).getValues()
            i = getDataBasedOnFileName(table)

            return render(request, 'app_cmp/fileList.1.html', {'files': i})

    else:
        print(form.errors)

    return render(request, 'app_cmp/index.1.html', {'form': form})


def displayFile(request, value):
    def initial_letter_filter(text,  autoescape=True):
        result = "<span style=\"color:red\">" + str(text) + "</span>"
        return mark_safe(result)

    vals = TempTable.objects.filter(FileID=value)
    path = str(vals[0].RootPath) + "//" + str(vals[0].FileName)
    lineNumber = vals[0].lineNumber
    context_val = []
    i = 1
    with open(path) as fp:
        line = fp.readline()
        if i == int(lineNumber):
            x = initial_letter_filter(str(i) + ". " + line.replace('\n', ""))
            print("ddd" + x)
            context_val.append(x)
        else:
            context_val.append(str(i) + ". " + line.replace('\n', ""))
        while line:
            i += 1
            line = fp.readline()
            if i == int(lineNumber):
                x = initial_letter_filter(
                    str(i) + ". " + line.replace('\n', ""))
                context_val.append(x)
            else:
                context_val.append(str(i) + ". " + line.replace('\n', ""))
    return render(request, 'app_cmp/files.1.html', {'code': context_val})


def displayFilePlain(request, value):
    vals = FileTable.objects.filter(FileID=value)
    path = str(vals[0].RootPath) + "//" + str(vals[0].FileName)
    print(path)
    context_val = []
    i = 1
    with open(path) as fp:
        line = fp.readline()
        context_val.append(str(i) + ". " + line.replace('\n', ""))
        while line:
            i += 1
            line = fp.readline()
            context_val.append(str(i) + ". " + line.replace('\n', ""))
    return render(request, 'app_cmp/file.1.html', {'code': context_val})


def populateDB(request):
    form = SearchForms()
    xx = pop.filesToDB().populate()
    return redirect('index')
