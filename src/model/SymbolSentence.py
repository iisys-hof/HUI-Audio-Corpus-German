from typing import List
from ttsCode.src.utils.ModelToStringConverter import ToString

class SymbolSentence(ToString):
    def __init__ (self, sentence: List[int]):
        self.sentence = sentence