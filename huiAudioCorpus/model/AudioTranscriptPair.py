from huiAudioCorpus.utils.ModelToStringConverter import ToString
from huiAudioCorpus.model.Sentence import Sentence
from huiAudioCorpus.model.Audio import Audio

class AudioTranscriptPair(ToString):
    
    def __init__(self, sentence: Sentence, audio: Audio):
        self.sentence = sentence
        self.audio = audio