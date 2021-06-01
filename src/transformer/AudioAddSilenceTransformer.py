import numpy as np
from ttsCode.src.model.Audio import Audio


class AudioAddSilenceTransformer:

    def __init__(self,startDurationSeconds: float,  endDurationSeconds: float):
        self.startDurationSeconds = startDurationSeconds
        self.endDurationSeconds = endDurationSeconds

    def transform(self, audio: Audio):
        silenceAudioFront = self.generateSilence(self.startDurationSeconds, audio.samplingRate)
        silenceAudioBack = self.generateSilence(self.endDurationSeconds, audio.samplingRate)
        newAudio = silenceAudioFront+ audio + silenceAudioBack
        return newAudio

    def generateSilence(self,duration: float, samplingRate: int):
        silenceDataPoints = int(duration*samplingRate)
        silence = np.zeros(silenceDataPoints)
        silenceAudio =  Audio(silence, samplingRate, 's', 's')
        return silenceAudio
