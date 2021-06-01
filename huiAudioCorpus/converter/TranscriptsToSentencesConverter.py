
from pathlib import Path
from huiAudioCorpus.model.Sentence import Sentence
from huiAudioCorpus.model.Transcripts import Transcripts

class TranscriptsToSentencesConverter:
    def convert(self, transcripts: Transcripts):
        texts = transcripts.text
        ids = transcripts.keys
        sentences = [Sentence(text, Path(id).stem) for text, id in zip(texts, ids)]
        return sentences