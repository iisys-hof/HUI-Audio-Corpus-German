from os import error
from textblob import TextBlob
from ttsCode.src.utils.ModelToStringConverter import ToString
from typing import List

class Sentence(ToString):
    def __init__(self, sentence: str, id: str = ''):
        sentence = self.cleanSpaces(sentence)
        sentence = self.cleanSpacesPunctuation(sentence)

        self.sentence = sentence
        self.id = id

        textBlob = TextBlob(self.sentence.replace('.',' . ') )
        self.words = self.generateWords(textBlob)
        self.wordsWithoutChars: List[str] = [word.lower() for word in textBlob.words] # type: ignore
        self.wordsWithoutCharsAndUpperChars: List[str] = [word for word in textBlob.words] # type: ignore
        self.wordsCount = len(self.wordsWithoutChars)
        self.charCount = len(self.sentence)
        self.wordsMatchingWithChars = self.generateWordsMatchingWithChars(self.words ,self.wordsWithoutChars)
        self.rawChars = "".join(self.wordsWithoutChars)

    def generateWords(self, textBlob:TextBlob):
        words = list(textBlob.tokenize())

        return words
    def __getitem__(self, k):

        return Sentence(" ".join(self.wordsMatchingWithChars[k]))

    def generateWordsMatchingWithChars(self, words:List[str], wordsWithoutChars: List[str]):
        wordMatching = []
        wordPointer = 0
        for word in words:
            if wordPointer<len(wordsWithoutChars) and wordsWithoutChars[wordPointer] == word.lower():
                wordPointer+=1
                wordMatching.append(word)
            else:
                if len(wordMatching[-1]) > 1000:
                    print(wordMatching[-1])
                    raise Exception("Problems during creation of word matchings.")
                wordMatching[-1]+=' ' + word
        return wordMatching


    def cleanSpaces(self, text: str):
        text =  text.replace('  ', ' ').replace('  ',' ').replace('  ',' ').replace('  ',' ')
        return text

    def cleanSpacesPunctuation(self, text: str):
        punctuations = '.,;?!:"'
        for char in punctuations:
            text = text.replace(char, char+' ')
        for char in punctuations:
            text = text.replace(' ' + char,char)
        text = text.replace('  ', ' ').replace('  ', ' ')
        return text.strip()