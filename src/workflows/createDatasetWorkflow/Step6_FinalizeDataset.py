from ttsCode.src.transformer.TranscriptsSelectionTransformer import TranscriptsSelectionTransformer
import pandas as pd
from ttsCode.src.model.Audio import Audio
from ttsCode.src.utils.DoneMarker import DoneMarker
from ttsCode.src.persistenz.AudioPersistenz import AudioPersistenz
from ttsCode.src.persistenz.TranscriptsPersistenz import TranscriptsPersistenz
from tqdm import tqdm

class Step6_FinalizeDataset:

    def __init__(self, savePath: str,chapterPath: str, audioPersistenz: AudioPersistenz, transcriptsPersistenz: TranscriptsPersistenz, transcriptsSelectionTransformer: TranscriptsSelectionTransformer):
        self.savePath = savePath
        self.audioPersistenz = audioPersistenz
        self.transcriptsPersistenz = transcriptsPersistenz
        self.chapterPath = chapterPath
        self.transcriptsSelectionTransformer = transcriptsSelectionTransformer
    
    
    def run(self):
        doneMarker = DoneMarker(self.savePath)
        result = doneMarker.run(self.script, deleteFolder=False)
        return result

    def script(self):
        transcriptsIterator = list(self.transcriptsPersistenz.loadAll())
        transcripts = transcriptsIterator[0]
        transcriptsIds = [sentence.id for sentence in transcripts.sentences()]
        chapters = pd.read_csv(self.chapterPath)

        transcriptsSelectedIds = {}

        ids = self.audioPersistenz.getIds()
        audios = self.audioPersistenz.loadAll()
        audio: Audio
        for audio in tqdm(audios, total=len(ids)):
            book, chapter, index  = audio.id.rsplit('_',2)
            reader:str = chapters.loc[int(chapter)-1]['Reader'] # type:ignore
            reader = reader.replace(' ', '_')
            if audio.id in transcriptsIds:
                path = reader + '/' + book
                if path in transcriptsSelectedIds:
                    transcriptsSelectedIds[path].append(audio.id)
                else:
                    transcriptsSelectedIds[path] = [audio.id]
                audio.id = path + '/wavs/' + audio.id
                self.audioPersistenz.save(audio)
        for path, ids in transcriptsSelectedIds.items():
            localTranscripts = self.transcriptsSelectionTransformer.transform(transcripts, ids)
            localTranscripts.id = path + '/metadata'
            self.transcriptsPersistenz.save(localTranscripts)