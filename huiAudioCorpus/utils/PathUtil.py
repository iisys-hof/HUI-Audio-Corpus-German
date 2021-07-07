from io import BufferedReader
import json
from pathlib import Path
import os
import huiAudioCorpus.testOutput as testOutput
from tqdm import tqdm 
import requests
from zipfile import ZipFile

class PathUtil:
    def filenameWithoutExtension(self, path:str):
        filename = self.filenameWithExtension(path)
        filenameWithoutExtension =os.path.splitext(filename)[0]
        return filenameWithoutExtension

    def filenameWithExtension(self, path: str):
        filename = Path(path).name
        return filename 

    def createFolderForFile(self,file):
        Path(file).parent.mkdir(parents=True, exist_ok=True)

    def deleteFolder(self, folder):
        if self.fileExists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                else:
                    self.deleteFolder(file_path)
            os.rmdir(folder)

    def getTestDataFolder(self, testFile: str):
        testFolder = testOutput.__path__[0] +'/' +  self.filenameWithoutExtension(testFile)
        return testFolder

    def copyFileWithStream(self, inputStream: BufferedReader, inputSize: int, outputFile):
        self.createFolderForFile(outputFile)
        bufferSize = 1024*1024*2

        with tqdm(total=inputSize, unit='iB', unit_scale=True, unit_divisor=1024) as pbar:
            with open(outputFile, 'wb') as dest:
                while True:
                    copy_buffer = inputStream.read(bufferSize)
                    if not copy_buffer:
                        break
                    size = dest.write(copy_buffer)
                    pbar.update(size)

    def copyFileFromUrl(self, url: str, outputFile):
        self.createFolderForFile(outputFile)
        bufferSize = 1024*10

        resp = requests.get(url, stream=True)
        inputSize = resp.headers.get('content-length')
        if inputSize is not None:
            inputSize = int(inputSize)
        else:
            inputSize = None

        inputSize = int()# type:ignore
        with tqdm(total=inputSize, unit='iB', unit_scale=True, unit_divisor=1024, desc=url) as pbar:
            with open(outputFile, 'wb') as dest:
                for data in resp.iter_content(chunk_size=bufferSize):
                    size = dest.write(data)
                    pbar.update(size)

    def copyFile(self, inputFile: str, outputFile: str):
        size = os.path.getsize(inputFile)
        with open(inputFile, 'rb',) as source:
            self.copyFileWithStream(source, size, outputFile)

    def unzip(self, inputZip:str, outputFolder:str):
        with ZipFile(inputZip, 'r') as zipReference:
            for file in zipReference.namelist():
                if not self.fileExists(outputFolder + '/' + file):
                    print('start unzipping because file ', file, 'does not exist.')
                    self.deleteFolder(outputFolder)
                    zipReference.extractall(outputFolder)
                    break

    def saveJson(self, filename:str, jsonContent):
        string = json.dumps(jsonContent, indent=4, ensure_ascii=False)
        self.createFolderForFile(filename)
        with open(filename, 'w', encoding='utf8') as file:
            file.write(string)

    def loadJson(self, filename: str):
        with open(filename, encoding='utf8') as jsonFile:
            data = json.load(jsonFile)
        return data

    def fileExists(self, filename):
        exists = os.path.exists(filename)
        return exists

    def writeFile(self, text: str, filename: str):
        self.createFolderForFile(filename)
        with open(filename, 'w', encoding='utf8') as f:
            f.write(text)

    def loadFile(self, filename: str):
        with open(filename, 'r', encoding='utf8') as f:
            inputText = f.read()
        return inputText