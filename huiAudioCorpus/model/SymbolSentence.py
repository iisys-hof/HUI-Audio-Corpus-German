from typing import List
from huiAudioCorpus.utils.ModelToStringConverter import ToString

class SymbolSentence(ToString):
    def __init__ (self, sentence: List[int]):
        self.sentence = sentence