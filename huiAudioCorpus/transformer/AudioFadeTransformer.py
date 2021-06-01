from huiAudioCorpus.model.Audio import Audio
import numpy as np

class AudioFadeTransformer:

    def __init__(self, fadeInDuration: float = 0.1, fadeOutDuration: float = 0.1):
        self.fadeInDuration = fadeInDuration
        self.fadeOutDuration = fadeOutDuration

    def transform(self, audio: Audio):
        audio = self.fadeOut(audio)
        audio = self.fadeIn(audio)
        return audio
        

    def fadeOut(self, audio: Audio) -> Audio: 
        countOfSamples= int(self.fadeOutDuration*audio.samplingRate)
        end = audio.samples
        start = end - countOfSamples

        # compute fade out curve
        # linear fade
        fade_curve = np.linspace(1.0, 0.0, countOfSamples)

        # apply the curve
        audio.timeSeries[start:end] = audio.timeSeries[start:end] * fade_curve
        return audio

    def fadeIn(self, audio: Audio) -> Audio: 
        countOfSamples= int(self.fadeOutDuration*audio.samplingRate)
        end = countOfSamples
        start = 0

        # compute fade out curve
        # linear fade
        fade_curve = np.linspace(0.0, 1.0, countOfSamples)

        # apply the curve
        audio.timeSeries[start:end] = audio.timeSeries[start:end] * fade_curve
        return audio