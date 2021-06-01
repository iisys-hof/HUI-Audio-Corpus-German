from ttsCode.src.model.PhoneticChars import PhoneticChars
from ttsCode.src.model.PhoneticSentence import PhoneticSentence
from ttsCode.src.model.SymbolSentence import SymbolSentence

class PhoneticSentenceToSymbolSentenceConverter:
    def __init__(self):
        self.symbols = PhoneticChars().chars
        self.symbol_to_id = {s: i for i, s in enumerate(self.symbols)}

    def convert(self, phoneticSentence:PhoneticSentence):
        sentence = phoneticSentence.sentence
        symbols = [self.getId(char) for char in sentence]
        return SymbolSentence(symbols)

    def getId(self, char):
            return self.symbol_to_id[char] +1