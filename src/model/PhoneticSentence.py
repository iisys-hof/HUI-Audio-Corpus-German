from typing import List
from ttsCode.src.utils.ModelToStringConverter import ToString

class PhoneticSentence(ToString):
    def __init__ (self, sentence: str, subWords: List[str]):
        self.sentence = sentence
        self.subWords = subWords