
from itertools import count
from typing import List
from ttsCode.src.model.Audio import Audio
from ttsCode.src.persistenz.TranscriptsPersistenz import TranscriptsPersistenz
from pandas.core.frame import DataFrame
from ttsCode.src.model.Transcripts import Transcripts
from ttsCode.src.persistenz.AudioPersistenz import AudioPersistenz
from ttsCode.src.converter.AudioToSentenceConverter import AudioToSentenceConverter
from ttsCode.src.utils.DoneMarker import DoneMarker
from tqdm import tqdm
import numpy as np
from joblib import Parallel, delayed

class Step4_TranscriptAudio:

    def __init__(self, savePath: str, audioToSentenceConverter: AudioToSentenceConverter, audioPersistenz: AudioPersistenz, transcriptsPersistenz: TranscriptsPersistenz, numberWorker = 4):
        self.savePath = savePath
        self.audioToSentenceConverter = audioToSentenceConverter
        self.audioPersistenz = audioPersistenz
        self.transcriptsPersistenz = transcriptsPersistenz
        self.numberWorker = numberWorker


    def run(self):
        return DoneMarker(self.savePath).run(self.script)
    
    def script(self):
        ids = self.audioPersistenz.getIds()
        chunks = np.array_split(ids, self.numberWorker)

        parallelResult = Parallel(n_jobs=self.numberWorker)(delayed(self.loadOneChunk)(audioIds, chunkId) for chunkId, audioIds in enumerate(chunks))

        results = [[sentence.id, sentence.sentence] for level in parallelResult for sentence in level]

        csv =  DataFrame(results)
        transcripts = Transcripts(csv, 'transcripts', 'transcripts')
        self.transcriptsPersistenz.save(transcripts)

    def loadOneChunk(self, ids: List[str], chunkId: int):
        sentences = []
        for id in tqdm(ids, desc="Chunk " + str(chunkId) + ": "):
            audio = self.audioPersistenz.load(id)
            sentence = self.audioToSentenceConverter.convert(audio)
            sentences.append(sentence)
        return sentences
