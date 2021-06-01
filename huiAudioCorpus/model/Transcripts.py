from huiAudioCorpus.model.Sentence import Sentence
from typing import List
from huiAudioCorpus.utils.ModelToStringConverter import ToString
from pandas.core.frame import DataFrame
class Transcripts(ToString):
    def __init__(self, transcripts: DataFrame, id: str, name: str):
        self.transcripts = transcripts
        self.id = id
        self.name = name
    

    @property
    def transcriptsCount(self):
        return self.transcripts.shape[0]

    @property
    def example(self):
        return self.transcripts.values[0][0]

    @property
    def keys(self) -> List[str]:
        #TODO: This is not generalizable at all! We should introduce column labels
        return list(self.transcripts[0].values) # type:ignore

    @property
    def text(self)-> List[str]:
        #TODO: This is not generalizable at all! We should introduce column labels
        return list(self.transcripts[self.transcripts.columns[-1]].values) # type:ignore

    
    def sentences(self) -> List[Sentence]:
        sentences = []
        for key, text in zip(self.keys, self.text):
            if type(text) == str:
                sentences.append(Sentence(text,key))
        return sentences