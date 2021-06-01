from huiAudioCorpus.model.Sentence import Sentence
from Levenshtein import distance as LevensteinDistance

class SentenceDistanceTransformer:

    def transform(self, sentence1: Sentence, sentence2: Sentence):

        baseDistance = self.distanceTwoSentences(sentence1, sentence2)
        return baseDistance

  
    def distanceTwoSentences(self, sentence1: Sentence, sentence2: Sentence):
        if sentence1.wordsCount == 0 or sentence2.wordsCount == 0:
            return 1
        
        sentenceString1 = "".join(sentence1.wordsWithoutChars)
        sentenceString2 = "".join(sentence2.wordsWithoutChars)

        countCharsMax = max(len(sentenceString1) , len(sentenceString2))
        diff = LevensteinDistance(sentenceString1, sentenceString2)
        distance = diff / countCharsMax
        return distance
