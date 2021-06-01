from ttsCode.src.utils.ModelToStringConverter import ToString
from ttsCode.src.model.Sentence import Sentence

class SentenceAlignment(ToString):
    def __init__(self, sourceText: Sentence, alignedText: Sentence, start: int, end: int, distance: float, leftIsPerfekt:bool = False, rightIsPerfekt: bool = False, isFirst : bool = False, isLast: bool = False, isPerfect: bool = False, isSkipped: bool = False):
        self.sourceText = sourceText
        self.alignedText = alignedText
        self.start = start
        self.end = end
        self.distance = distance
        self.leftIsPerfekt = leftIsPerfekt
        self.rightIsPerfekt= rightIsPerfekt
        self.isFirst = isFirst
        self.isLast = isLast
        self.isPerfect = isPerfect
        self.isSkipped = isSkipped