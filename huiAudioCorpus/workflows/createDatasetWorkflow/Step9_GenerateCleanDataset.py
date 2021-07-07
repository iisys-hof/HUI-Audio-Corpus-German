
from huiAudioCorpus.utils.DoneMarker import DoneMarker
from huiAudioCorpus.transformer.TranscriptsSelectionTransformer import TranscriptsSelectionTransformer
from huiAudioCorpus.persistenz.TranscriptsPersistenz import TranscriptsPersistenz
from huiAudioCorpus.persistenz.AudioPersistenz import AudioPersistenz
from huiAudioCorpus.transformer.AudioSamplingRateTransformer import AudioSamplingRateTransformer
from tqdm.std import tqdm
import pandas as pd

class Step9_GenerateCleanDataset:

    def __init__(self, savePath: str, infoFile:str, audioPersistenz: AudioPersistenz, transcriptsPersistenz: TranscriptsPersistenz, audioSamplingRateTransformer: AudioSamplingRateTransformer, transcriptsSelectionTransformer: TranscriptsSelectionTransformer, filter):
        self.audioSamplingRateTransformer = audioSamplingRateTransformer
        self.audioPersistenz = audioPersistenz
        self.transcriptsPersistenz = transcriptsPersistenz
        self.transcriptsSelectionTransformer = transcriptsSelectionTransformer
        self.savePath = savePath
        self.infoFile = infoFile
        self.filter = filter

    def run(self):
        doneMarker = DoneMarker(self.savePath)
        result = doneMarker.run(self.script, deleteFolder=False)
        return result

    def script(self):
        df = pd.read_csv(self.infoFile, sep='|' , index_col=0)
        try:
            df = df.set_index('id')
        except:
            pass

        print('Audios bevore: ', df.shape[0])
        filteredAudios = self.filter(df)
        print('Audios after: ', filteredAudios.shape[0])
        audiosAllowed = filteredAudios.index.tolist()

        self.copyAudioFiles(audiosAllowed)
        self.copyAndFilterTranscripts(audiosAllowed)




    def copyAudioFiles(self, audiosAllowed):
        countFiles = len(self.audioPersistenz.getIds())
        for audio in tqdm(self.audioPersistenz.loadAll(), total= countFiles):
            if audio.name in audiosAllowed:
                self.audioPersistenz.save(audio)

    def copyAndFilterTranscripts(self, usedAudioFileNames):
        for transcripts in tqdm(self.transcriptsPersistenz.loadAll()):
            filteredTranscript = self.transcriptsSelectionTransformer.transform(transcripts, usedAudioFileNames)
            self.transcriptsPersistenz.save(filteredTranscript)