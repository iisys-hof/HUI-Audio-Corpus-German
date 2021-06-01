from ttsCode.src.model.Transcripts import Transcripts
from pandas.core.frame import DataFrame
from ttsCode.src.model.Sentence import Sentence
from ttsCode.src.calculator.AlignSentencesIntoTextCalculator import AlignSentencesIntoTextCalculator
from ttsCode.src.persistenz.TranscriptsPersistenz import TranscriptsPersistenz
from ttsCode.src.utils.DoneMarker import DoneMarker

class Step5_AlignText:

    def __init__(self, savePath: str, alignSentencesIntoTextCalculator: AlignSentencesIntoTextCalculator, transcriptsPersistenz: TranscriptsPersistenz, textToAlignPath: str):
        self.savePath = savePath
        self.alignSentencesIntoTextCalculator = alignSentencesIntoTextCalculator
        self.transcriptsPersistenz = transcriptsPersistenz
        self.textToAlignPath = textToAlignPath

    def run(self):
        doneMarker = DoneMarker(self.savePath)
        result = doneMarker.run(self.script, deleteFolder=False)
        return result

    def script(self):
        transcripts = list(self.transcriptsPersistenz.loadAll())
        sentences = transcripts[0].sentences()
        with open(self.textToAlignPath, 'r', encoding='utf8') as f:
            inputText = f.read()
        inputSentence = Sentence(inputText)
        
        alignments = self.alignSentencesIntoTextCalculator.calculate(inputSentence,sentences )
        notPerfektAlignments = [align for align in alignments if not align.isPerfect and not align.isSkipped]
        for align in notPerfektAlignments:
            print('------------------')
            print(align.sourceText.id)
            print(align.alignedText.sentence)
            print(align.sourceText.sentence)
            print(align.leftIsPerfekt)
            print(align.rightIsPerfekt)
            print(align.distance)

        print("notPerfektAlignments Percent",len(notPerfektAlignments)/len(alignments)*100)

        results = [[align.sourceText.id, align.alignedText.sentence]for align in alignments  if align.isPerfect]

        csv =  DataFrame(results)
        transcripts = Transcripts(csv, 'transcripts', 'transcripts')
        self.transcriptsPersistenz.save(transcripts)

        resultsNotPerfect = [[align.sourceText.id, align.alignedText.sentence]for align in alignments  if not align.isPerfect]

        csv =  DataFrame(resultsNotPerfect)
        transcripts = Transcripts(csv, 'transcriptsNotPerfect', 'transcriptsNotPerfect')
        self.transcriptsPersistenz.save(transcripts)
