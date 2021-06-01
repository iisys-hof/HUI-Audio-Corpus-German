from ttsCode.src.model.Audio import Audio
from typing import List

class AudioFilter:

    def __init__(self, maxDuration = None, names: List[str] = None):

        self.maxDuration = float('inf') if maxDuration is None else maxDuration
        self.names = names

    
    def isAllowed(self, audio: Audio):
        if audio.duration >= self.maxDuration:
            return False
        if self.names is not None and audio.name not in self.names:
            return False
        return True

    def filter(self, audios: List[Audio]):
        filteredAudios = [audio for audio in audios if self.isAllowed(audio)]
        return filteredAudios
