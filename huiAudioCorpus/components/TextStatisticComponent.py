from tqdm import tqdm  
from huiAudioCorpus.converter.ListToHistogramConverter import ListToHistogramConverter
from huiAudioCorpus.converter.ListToStatisticConverter import ListToStatisticConverter
from huiAudioCorpus.persistenz.TranscriptsPersistenz import TranscriptsPersistenz
from huiAudioCorpus.converter.TranscriptsToSentencesConverter import TranscriptsToSentencesConverter
from pandas.core.frame import DataFrame
from collections import Counter
from huiAudioCorpus.model.Sentence import Sentence

class TextStatisticComponent:
    def __init__(self, transcriptsPersistenz: TranscriptsPersistenz, transcriptsToSentencesConverter:TranscriptsToSentencesConverter, listToStatisticConverter:ListToStatisticConverter, listToHistogramConverter: ListToHistogramConverter):
        self.transcriptsPersistenz = transcriptsPersistenz
        self.transcriptsToSentencesConverter = transcriptsToSentencesConverter
        self.listToStatisticConverter = listToStatisticConverter
        self.listToHistogramConverter = listToHistogramConverter

    def run(self):
        rawData= self.loadTextFiles()
        return self.getStatistic(rawData)

    def getStatistic(self, rawData):
        descriptions = ['Words count in audio', 'Chars count in audio']
        ids = ['wordCount', 'charCount']
        statistics = {}
        for column in rawData:
            if column not in ids:
                continue
            statistics[column] = {
                'name': column,
                'statistic': self.listToStatisticConverter.convert(rawData[column].tolist()),
                'histogram': self.listToHistogramConverter.convert(rawData[column].tolist()),
                'description': descriptions[len(statistics)]
            }


        if 'text' not in rawData:
            counter = Counter()
            uniqeWordsWithMinimum = {}

        else:
            counter = Counter([word for sentence in tqdm(rawData['text']) for word in Sentence(sentence).wordsWithoutChars])

            counterValues = counter.values()
            uniqeWordsWithMinimum = {}
            remainingCounts = counterValues
            for minWortOccurence  in tqdm(list(range(1, max(counterValues)+1))): 
                remainingCounts = [count for count in remainingCounts if count>=minWortOccurence]
                uniqeWordsWithMinimum[minWortOccurence] = len(remainingCounts)
                if(len(remainingCounts)==1):
                    break

        return statistics, rawData, counter, uniqeWordsWithMinimum

    def loadTextFiles(self):
        allSentences =[sentence for transcripts in tqdm(self.transcriptsPersistenz.loadAll(), total=len(self.transcriptsPersistenz.getIds())) for sentence in  self.transcriptsToSentencesConverter.convert(transcripts)]
        result =  [[sentence.id.split("\\")[-1].split("/")[-1], sentence.wordsCount, sentence.charCount, sentence.sentence] for sentence in  tqdm(allSentences)]
        rawData = DataFrame(result, columns  = ['id','wordCount', 'charCount', 'text'])
        rawData = rawData.set_index('id')
        return rawData