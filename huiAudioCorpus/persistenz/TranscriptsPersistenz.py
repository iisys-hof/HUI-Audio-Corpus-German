from pandas.core.frame import DataFrame
from huiAudioCorpus.model.Transcripts import Transcripts
from huiAudioCorpus.utils.FileListUtil import FileListUtil
from huiAudioCorpus.utils.PathUtil import PathUtil
import pandas as pd

class TranscriptsPersistenz:
    def __init__(self, loadPath:str, savePath: str = None, fileExtension:str = 'csv'):
        self.savePath = loadPath if savePath is None else savePath
        self.loadPath = loadPath
        self.fileExtension = fileExtension
        self.fileListUtil = FileListUtil()
        self.pathUtil = PathUtil()

    def getIds(self):
        transcriptsFiles = self.fileListUtil.getFiles(self.loadPath, self.fileExtension)
        transcriptsFiles = [file.replace(self.loadPath,'')[1:-len(self.fileExtension)-1] for file in transcriptsFiles]
        return transcriptsFiles
    
    def load(self, id: str):
        targetPath = self.loadPath +'/' +  id + '.' + self.fileExtension
        csv: DataFrame
        csv = pd.read_csv(targetPath, sep='|', header=None) # type: ignore
        name = self.pathUtil.filenameWithoutExtension(targetPath)
        transcripts = Transcripts(csv, id, name)
        return transcripts
    
    def save(self, transcripts: Transcripts):
        targetPath = self.savePath +'/' +  transcripts.id + '.' + self.fileExtension
        self.pathUtil.createFolderForFile(targetPath)
        trans = transcripts.transcripts
        trans.to_csv(targetPath, sep='|', header = None, index=False) # type: ignore

    def loadAll(self):
        ids = self.getIds()
        for id in ids:
            yield self.load(id)