import librosa
from huiAudioCorpus.model.Audio import Audio


class AudioRemoveSilenceTransformer:

    def __init__(self, dezibel: int):
        self.dezibel = dezibel

    def transform(self, audio: Audio):
        newAudioTimeline,_ = librosa.effects.trim(audio.timeSeries, self.dezibel)
        newAudio = Audio(newAudioTimeline, audio.samplingRate, audio.id, audio.name)
        return newAudio