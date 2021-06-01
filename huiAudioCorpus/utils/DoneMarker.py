import os
from datetime import datetime
from os import unlink
from os.path import isfile
from huiAudioCorpus.enum.PipelineReturnEnum import PipelineReturnEnum
from huiAudioCorpus.utils.PathUtil import PathUtil

class DoneMarker:
    doneFilename = '.done'
    
    def __init__(self, path: str):
        self.path = path
        self.doneFilePath = path + '/' + self.doneFilename
        self.pathUtil = PathUtil()

    def isDone(self):
        isDone = os.path.exists(self.doneFilePath)
        return isDone

    def setDone(self):
        self.pathUtil.createFolderForFile(self.doneFilePath)
        f = open(self.doneFilePath, "w")
        f.write(f'Done at:   {datetime.now()}')
        f.close()

    def remove(self):
        if isfile(self.doneFilePath):
            unlink(self.doneFilePath)

    def getInfo(self):
        return 'Continue to next step because of done marker.'

    def run(self, script, deleteFolder = True):
        if self.isDone():
            print(self.getInfo())
            return PipelineReturnEnum.OkWithDoneMarker

        if deleteFolder:
            self.pathUtil.deleteFolder(self.path)

        script()

        self.setDone()
        return PipelineReturnEnum.Ok