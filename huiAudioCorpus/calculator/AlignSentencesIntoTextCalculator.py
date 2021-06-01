import operator
from nltk.sem.evaluate import Error
from tqdm import tqdm
from huiAudioCorpus.model.SentenceAlignment import SentenceAlignment
from typing import List
from huiAudioCorpus.model.Sentence import Sentence
from huiAudioCorpus.transformer.SentenceDistanceTransformer import SentenceDistanceTransformer
from joblib import Parallel, delayed

rangeWords = 40
class AlignSentencesIntoTextCalculator:

    def __init__(self, sentenceDistanceTransformer: SentenceDistanceTransformer):
        self.sentenceDistanceTransformer = sentenceDistanceTransformer

    def calculate(self, originalText: Sentence, textToAlign: List[Sentence]):

        alignments = self.calculateAlignments(originalText,textToAlign)
        alignments = self.evaluateIfPerfektStartAndEnd(alignments,originalText.wordsCount)
        alignments = self.getMissingWordsBetweenAlignments(alignments, originalText)
        return alignments

    def calculateAlignments(self, originalText: Sentence, textToAlign: List[Sentence]):
        with Parallel(n_jobs=15, batch_size=500) as parallel:
            alignments:List[SentenceAlignment] = []
            start=0
            text: Sentence
            additionalRange =  0
            for text in tqdm(textToAlign):


                rangeStart= max(0,start-rangeWords - additionalRange)
                rangeEnd = min(rangeStart+2*(rangeWords + additionalRange)+text.wordsCount,originalText.wordsCount+1)

                if rangeEnd- rangeStart>2000:
                    raise Exception('more than 2000 Words in search text')

                (newStart, end), distance = self.bestPosition(parallel,originalText[rangeStart: rangeEnd ], text, 0, rangeEnd- rangeStart)
                newStart += rangeStart
                end += rangeStart

                align = SentenceAlignment(text, originalText[newStart: end],newStart, end, distance)
                if distance>0.2:
                    print('*****************')
                    print('skip because of too high distance: ',text.id, distance)
                    print('*****************')
                    print(text.sentence)
                    print('___________________')
                    print(originalText[rangeStart: rangeEnd ].sentence)
                    print('########')

                    align.isSkipped = True
                    additionalRange += 30 + text.wordsCount
                else: 
                    start = end
                    additionalRange= 0
                alignments.append(align)
            return alignments

    def bestPosition(self,parallel:Parallel, originalText: Sentence, textToAlign: Sentence, rangeStart: int, rangeEnd: int):
        startEnds = []
        for end in range(rangeStart, rangeEnd):
            for start in range(max(rangeStart,end-textToAlign.wordsCount-10), end):
                startEnds.append((start, end))

        positionene = parallel(delayed(self.positionOneSentence)(originalText, textToAlign, start, end) for start, end in startEnds)
        #positionene = [self.positionOneSentence(originalText, textToAlign, start, end) for start, end in startEnds]
        
        bestPosition = min(positionene, key=operator.itemgetter(1)) # type: ignore
        return  bestPosition

    def positionOneSentence(self, originalText: Sentence , textToAlign: Sentence, start: int, end: int):
        textToSearch = originalText[start:end]
        distance = self.sentenceDistanceTransformer.transform(textToSearch, textToAlign)
        return [(start, end), distance]


    def evaluateIfPerfektStartAndEnd(self,alignments:  List[SentenceAlignment], originalTextLength: int):
        for index, align in enumerate(alignments):
            align.leftIsPerfekt = False
            align.rightIsPerfekt = False
            align.isFirst = index ==0
            align.isLast = index == len(alignments)-1

            if align.start==0:
                align.leftIsPerfekt=True
            if align.end == originalTextLength:
                align.rightIsPerfekt= True

            try:
                if align.start == alignments[index-1].end:
                    align.leftIsPerfekt=True
            except:
                pass
            try:
                if align.end == alignments[index+1].start:
                    align.rightIsPerfekt=True
            except:
                pass
            align.isPerfect = (align.leftIsPerfekt or align.isFirst) and (align.rightIsPerfekt or align.isLast) and not align.isSkipped
        return alignments

    def getMissingWordsBetweenAlignments(self, alignments:  List[SentenceAlignment], originalText: Sentence):
        for index, aling in enumerate(alignments):
            if index == len(alignments)-1:
                continue
            
            if not aling.rightIsPerfekt:
                print(originalText[aling.end:alignments[index+1].start])

        return alignments