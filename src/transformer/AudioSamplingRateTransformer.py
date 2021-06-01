import librosa
from ttsCode.src.model.Audio import Audio


class AudioSamplingRateTransformer():

    def __init__(self, targetSamplingRate: int = None):
        self.targetSamplingRate = targetSamplingRate

    def transform(self, audio: Audio ):
        if self.targetSamplingRate is None:
            return audio
        if audio.samplingRate == self.targetSamplingRate:
            return audio
        audioTimeSeries = audio.timeSeries
        samplingRate = audio.samplingRate
        resampledTimeSeries = librosa.core.resample(audioTimeSeries, samplingRate, self.targetSamplingRate)
        resampledAudio = Audio(resampledTimeSeries, self.targetSamplingRate, audio.id, audio.name) # type:ignore
        return resampledAudio
