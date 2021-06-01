

from typing import List
from ttsCode.src.persistenz.AudioPersistenz import AudioPersistenz
from ttsCode.src.transformer.AudioSplitTransformer import AudioSplitTransformer
from ttsCode.src.transformer.AudioLoudnessTransformer import AudioLoudnessTransformer
from ttsCode.src.model.Audio import Audio
from ttsCode.src.utils.DoneMarker import DoneMarker
from joblib import Parallel, delayed

class Step2_SplitAudio:

    def __init__(self, audioSplitTransformer:AudioSplitTransformer , audioPersistenz: AudioPersistenz, savePath: str, bookName: str, audioLoudnessTransformer: AudioLoudnessTransformer, remapSort: List[int] = None):
        self.audioPersistenz = audioPersistenz
        self.savePath = savePath
        self.audioSplitTransformer = audioSplitTransformer
        self.bookName = bookName
        self.audioLoudnessTransformer = audioLoudnessTransformer
        self.remapSort = remapSort

    def run(self):
        return DoneMarker(self.savePath).run(self.script)
    
    def script(self):
        audios = self.audioPersistenz.loadAll()
        if self.remapSort:
            audios = list(audios)
            audios = [audios[i] for i in self.remapSort]

        Parallel(n_jobs=1, verbose=10, batch_size= 100)(delayed(self.splitOneAudio)(audio, index) for index, audio in enumerate(audios))


    def splitOneAudio(self, audio: Audio, index:int):
        splittedAudios = self.audioSplitTransformer.transform(audio, self.bookName, index+1)
        for splitAudio in splittedAudios:
            loudnessAudio = self.audioLoudnessTransformer.transform(splitAudio)
            self.audioPersistenz.save(loudnessAudio)