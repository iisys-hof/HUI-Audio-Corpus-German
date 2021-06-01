from ttsCode.src.model.AudioTranscriptPair import AudioTranscriptPair
from ttsCode.src.error.MatchingNotFoundError import MatchingNotFoundError
from typing import List
from ttsCode.src.converter.TranscriptsToSentencesConverter import TranscriptsToSentencesConverter
from ttsCode.src.persistenz.AudioPersistenz import AudioPersistenz
from ttsCode.src.persistenz.TranscriptsPersistenz import TranscriptsPersistenz

class AudioTranscriptPairPersistenz:

    def __init__(self, audioPersistenz: AudioPersistenz, transcriptsPersistenz: TranscriptsPersistenz, transcriptsToSentencesConverter: TranscriptsToSentencesConverter, checkForConsistency:bool = True):
        self.audioPersistenz = audioPersistenz
        self.transcriptsPersistenz = transcriptsPersistenz
        self.transcriptsToSentencesConverter = transcriptsToSentencesConverter

    def load(self, audioId: str, sentenceId:str):
        audio = self.audioPersistenz.load(audioId)
        sentence = self.getAllSentences()[sentenceId]
        elementPair = AudioTranscriptPair(sentence, audio)
        return elementPair


    def getIds(self, checkForConsistency = True):
        audioIds = self.audioPersistenz.getIds()
        audioNames = self.audioPersistenz.getNames()
        sentencesIds = list(self.getAllSentences().keys())

        if checkForConsistency:
            self.checkeIds(audioNames, sentencesIds)
        else:
            audioIds,audioNames, sentencesIds = self.removeNonExistentIds(audioIds, audioNames, sentencesIds)
  
        ids = self.sortIds(audioIds, audioNames, sentencesIds)   
        
        return ids

    def sortIds(self, audioIds, audioNames, sentencesIds):
        zippedAudios = list(zip(audioIds, audioNames))
        zippedAudios.sort(key = lambda x: x[1])
        audioIds = [element[0] for element in zippedAudios]
        sentencesIds.sort()
        return list(zip(audioIds, sentencesIds))
        

    def loadAll(self, checkForConsistency = True):
        ids = self.getIds(checkForConsistency)
        for audioId, sentenceId in ids:
            yield self.load(audioId, sentenceId)


    def getAllSentences(self):
        transcripts = list(self.transcriptsPersistenz.loadAll())
        sentences = [sentence for transcript in transcripts for sentence in self.transcriptsToSentencesConverter.convert(transcript)]
        sentenceDict = {sentence.id: sentence for sentence in sentences}
        return sentenceDict

    def checkeIds(self, audioIds: List[str], sentenceIds: List[str]):
        missingAudioIds = [id for id in sentenceIds if not id in audioIds]
        missingSentenceIds = [id for id in audioIds if not id in sentenceIds]
        if missingAudioIds or missingSentenceIds:
            raise MatchingNotFoundError(missingAudioIds, missingSentenceIds, 'audioFiles', 'Transcripts')

    def removeNonExistentIds(self, audioIds: List[str], audioNames: List[str], sentenceIds: List[str]):
        audioIds = [id for id, name in zip(audioIds, audioNames) if name in sentenceIds]
        audioNames = [name for name in  audioNames if name in sentenceIds]
        sentenceIds= [id for id in sentenceIds if id in audioNames]
        return audioIds, audioNames, sentenceIds