from ttsCode.src.utils.ModelToStringConverter import ToString
from ttsCode.src.model.Sentence import Sentence
from ttsCode.src.model.Audio import Audio

class AudioTranscriptPair(ToString):
    
    def __init__(self, sentence: Sentence, audio: Audio):
        self.sentence = sentence
        self.audio = audio