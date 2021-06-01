
from pathlib import Path
from ttsCode.src.model.Sentence import Sentence
from ttsCode.src.model.Transcripts import Transcripts

class TranscriptsToSentencesConverter:
    def convert(self, transcripts: Transcripts):
        texts = transcripts.text
        ids = transcripts.keys
        sentences = [Sentence(text, Path(id).stem) for text, id in zip(texts, ids)]
        return sentences