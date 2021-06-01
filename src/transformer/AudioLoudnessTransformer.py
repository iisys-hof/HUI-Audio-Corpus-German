from ttsCode.src.model.Audio import Audio
import pyloudnorm as pyln


class AudioLoudnessTransformer:

    def __init__(self, loudness: int):
        self.loudness = loudness

    def transform(self, audio: Audio):
        meter = pyln.Meter(audio.samplingRate) # create BS.1770 meter

        loudnessNormalizedAudio = pyln.normalize.loudness(audio.timeSeries, audio.loudness, self.loudness)
        newAudio = Audio(loudnessNormalizedAudio, audio.samplingRate, audio.id, audio.name)
        return newAudio