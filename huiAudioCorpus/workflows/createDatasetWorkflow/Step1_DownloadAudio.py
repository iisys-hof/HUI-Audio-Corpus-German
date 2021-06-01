

from huiAudioCorpus.persistenz.AudiosFromLibrivoxPersistenz import AudiosFromLibrivoxPersistenz
from huiAudioCorpus.utils.DoneMarker import DoneMarker


class Step1_DownloadAudio:

    def __init__(self, audiosFromLibrivoxPersistenz: AudiosFromLibrivoxPersistenz, savePath: str):
        self.savePath = savePath
        self.audiosFromLibrivoxPersistenz = audiosFromLibrivoxPersistenz

    def run(self):
        return DoneMarker(self.savePath).run(self.script)
    
    def script(self):
        self.audiosFromLibrivoxPersistenz.save()

