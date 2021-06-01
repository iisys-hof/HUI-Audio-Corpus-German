from typing import List
import librosa
from ttsCode.src.model.Audio import Audio
from ttsCode.src.transformer.AudioFadeTransformer import AudioFadeTransformer
import statistics

class AudioSplitTransformer:

    def __init__(self, audioFadeTransformer: AudioFadeTransformer, maxAudioDuration: float, minAudioDuration: float, silenceDurationInSeconds:float= 0.2):
        self.maxAudioDuration = maxAudioDuration
        self.minAudioDuration = minAudioDuration
        self.silenceDurationInSeconds = silenceDurationInSeconds
        self.audioFadeTransformer = audioFadeTransformer

    def transform(self, audio: Audio, bookName: str, chapter: int):
        splitted = self.splitWithBestDezibel(audio, self.maxAudioDuration - self.minAudioDuration)
        splitted = self.mergeAudioToTargetDuration(splitted, self.minAudioDuration)
        merged = self.mergeLastAudioIfTooShort(splitted, self.minAudioDuration)
        withIds = self.setIds(merged, bookName, chapter)
        withFading = self.fade(withIds)
        return withIds

    def splitWithBestDezibel(self, audio: Audio, maxAudioDuration: float):
        # TODO: think about using recrusive and split just needed audio files????
        splittedAudio:List[Audio]=[]
        maxDuration:float = 0
        for silenceDezibel in range(70, -20,-5):
            splittedAudio = self.split(audio, silenceDezibel)
            maxDuration = max([audio.duration for audio in splittedAudio])
            if maxDuration< maxAudioDuration:
                print( audio.name, 'used DB:', silenceDezibel)
                return splittedAudio
        return splittedAudio

    def split(self, audio: Audio, silenceDezibel: int):
        frameLength = int(self.silenceDurationInSeconds* audio.samplingRate)
        splitted = librosa.effects.split(audio.timeSeries,silenceDezibel , frame_length=frameLength, hop_length=int(frameLength/4))
        audios = []
        for index in range(len(splitted)):
            (start,end) = splitted[index]
            isNextElementAvailable = len(splitted)> index+1
            if isNextElementAvailable: 
                (nextStart, nextEnd) = splitted[index+1]
                betterEnd = int(statistics.mean([end, nextStart]))
            else:
                betterEnd = end

            isPreviousElementAvailable = not index == 0
            if isPreviousElementAvailable:
                (previousStart, previousEnd) = splitted[index-1]
                betterStart = int(statistics.mean([previousEnd, start]))
            else:
                betterStart = start

            newAudio = Audio(audio.timeSeries[betterStart:betterEnd], audio.samplingRate, 'id', 'name')
            audios.append(newAudio)
        return audios

    def mergeAudioToTargetDuration(self, audios: List[Audio], targetDuration: float):
        mergedAudios: List[Audio] = []

        for audio in audios:
            if len(mergedAudios)>0 and mergedAudios[-1].duration<targetDuration:
                mergedAudios[-1] = mergedAudios[-1] + audio
            else:
                mergedAudios.append(audio)
        return mergedAudios

    def mergeLastAudioIfTooShort(self, audios: List[Audio], minDuration: float):
        if audios[-1].duration<minDuration:
            audios[-2] = audios[-2] + audios[-1]
            audios.pop()
        return audios

    def setIds(self, audios: List[Audio], bookName: str, chapter: int):
        for index, audio in enumerate(audios):
            name = f"{bookName}_{chapter:02d}_f{index+1:06d}"
            audio.id = name
            audio.name = name
        return audios

    def fade(self, audios: List[Audio]):
        return [self.audioFadeTransformer.transform(audio) for audio in audios]