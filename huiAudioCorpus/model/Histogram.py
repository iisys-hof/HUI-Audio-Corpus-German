from huiAudioCorpus.utils.ModelToStringConverter import ToString
from typing import List, TypeVar
number = TypeVar('number', int, float)

class Histogram(ToString):
    def __init__(self, bins: List[number], values: List[number]):
        self.bins = bins
        self.values = values
