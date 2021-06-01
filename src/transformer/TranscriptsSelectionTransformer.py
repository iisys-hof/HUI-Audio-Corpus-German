from typing import List
from ttsCode.src.model.Transcripts import Transcripts

class TranscriptsSelectionTransformer:

    def transform(self, transcripts: Transcripts, selectedKeys: List[str]):
        trans = transcripts.transcripts
        transformedTrans = trans[trans[0].isin(selectedKeys)]# type:ignore
        transformedTranscripts = Transcripts(transformedTrans, transcripts.id, transcripts.name)
        return transformedTranscripts
