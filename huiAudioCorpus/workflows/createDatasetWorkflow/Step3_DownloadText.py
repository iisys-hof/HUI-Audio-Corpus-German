
from huiAudioCorpus.persistenz.GutenbergBookPersistenz import GutenbergBookPersistenz
from huiAudioCorpus.utils.DoneMarker import DoneMarker

class Step3_DownloadText:

    def __init__(self, GutenbergBookPersistenz: GutenbergBookPersistenz, savePath: str):
        self.savePath = savePath
        self.GutenbergBookPersistenz = GutenbergBookPersistenz

    def run(self):
        return DoneMarker(self.savePath).run(self.script)
    
    def script(self):
        self.GutenbergBookPersistenz.save()