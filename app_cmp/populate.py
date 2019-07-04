from app_cmp.models import PathTable, FileTable
import os

class File:
    root = ""
    fileName = ""
    extention = ""

    def __init__(self, root, fileName, extention):
        self.root = root
        self.fileName = fileName
        self.extention = extention


class filesToDB:
    def __init__(self):
        import django
        django.setup()


    def delete_everything(self):
        print("*****************dd")
        FileTable.objects.all().delete()
        PathTable.objects.all().delete()


    def populate(self):
        self.delete_everything()

        self.pathOfDirectory = "C:\\Users\\tyagi\\Desktop\\Language\\Python\\Algorithm"

        self.fileObj = list()
        i = 0

        for roots, directories, files in os.walk(self.pathOfDirectory):
            x = [".java", ".py", ".html"]
            for file in files:
                # fileComp stores the components of file, ie, filename and extention
                fileComp = os.path.splitext(file)

                if fileComp[1] in x:

                    # creating new File object for every file
                    self.fileObj.append(File(roots, fileComp[0] + fileComp[1], fileComp[1]))
                    i += 1

        print(str(i) + " file objects made.")
        for index in range(len(self.fileObj)):
            c = self.add_path(self.fileObj[index].root)
            self.add_file(c, self.fileObj[index].fileName, self.fileObj[index].extention)


    def add_path(self, path_str):
        p = PathTable.objects.get_or_create(Path=path_str)[0]
        # we need to save the changes we made!!
        p.save()
        return p


    def add_file(self, path, File="", Ext=""):
        c = FileTable.objects.get_or_create(
            RootPath=path, FileName=File, Extension=Ext)[0]
        print(c)
        c.save()
        return c
    
    def begin(self):
        populate()


# Start execution here!
if __name__ == '__main__':
    print("Starting population script...") 
