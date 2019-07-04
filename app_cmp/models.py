from django.db import models

class TempTable(models.Model):
    FileID = models.AutoField(primary_key=True)
    SearchTerm = models.CharField(max_length=250)
    RootPath = models.CharField(max_length=1000)
    FileName = models.CharField(max_length=250)
    lineNumber = models.CharField(max_length=50)
    CodeLine =  models.CharField(max_length=1000)

    def __str__(self):
        return self.FileName

class PathTable(models.Model):
    PathID = models.AutoField(primary_key=True)
    Path = models.TextField()

    def __str__(self):
        return self.Path


class FileTable(models.Model):
    FileID = models.AutoField(primary_key=True)
    RootPath = models.ForeignKey(PathTable, on_delete=models.PROTECT)
    FileName = models.CharField(max_length=250)
    Extension = models.CharField(max_length=50)

    def __str__(self):
        return self.FileName
