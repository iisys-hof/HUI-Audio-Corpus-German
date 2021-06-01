import glob

class FileListUtil:
    def getFiles(self,path: str, ending: str):
        searchPath = path +  '/**/*.' + ending
        files = glob.glob(searchPath, recursive=True)
        return files