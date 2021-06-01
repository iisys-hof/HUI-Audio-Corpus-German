from typing import List
from nltk.sem.evaluate import Error
from ttsCode.src.model.Sentence import Sentence
from ttsCode.src.model.PhoneticSentence import PhoneticSentence
import pandas as pd

class SentenceToPhoneticSentenceConverter:
    def __init__(self, libraryPath: str , useEmphasis: bool = True):
        self.library = self.createLibrary(libraryPath)
        self.useEmphasis = useEmphasis

    def convert(self, sentence: Sentence):
        words = sentence.words
        ipaWords, subWords = self.transformSentencesToIpa(words)
        ipaText = ' '.join(ipaWords)
        ipaText = self.removeEmphasis(ipaText)
        return PhoneticSentence(ipaText, subWords)


    def createLibrary(self, libraryPath: str):
        pointLibrary = pd.DataFrame({
            "text": [",", ".", "?", "-", ";", "!", ":", "'", "s", "ste", "(", ")", ">", "<", '›', '‹', 'é','è', '&'],
            "ipa": [",", ".","?", ",", ",", "!", ":", "'", "s", "stə", ",", ",", "'", "'", "'", "'", 'e', 'e', 'ʊnt']
        })
        library = pd.read_csv(libraryPath,keep_default_na=False)

        libraryLowerCase = library.copy(deep=True)
        libraryLowerCase['text'] = libraryLowerCase['text'].apply(str.lower)
        library = library.append(pointLibrary)
        library = library.append(libraryLowerCase)

        library.set_index('text', inplace = True)
        library.sort_index(inplace = True)
        return library

    def transformSentencesToIpa(self, words:List[str]):
            ipaWords: List[str] = []
            subWords: List[str] = []
            index = 0
            while index < len(words):
                word = words[index]
                remainingWords = words[index:]
                countMultiwords, multiwords, multiWord = self.findMultiwordIpa(remainingWords)
                if countMultiwords>0 and multiwords is not None:
                    index += countMultiwords
                    subWords.append(multiWord)
                    ipaWords.append(multiwords)
                    continue
                ipa, subWord = self.transformWordToIpa(word)
                subWords.append(subWord)
                ipaWords.append(ipa)
                index +=1
            return ipaWords, subWords
    
    def findMultiwordIpa(self, words:List[str]):
        if len(words)<2:
            return 0, None, ""
        for count in range(5,1,-1):
            multiWord = ' '.join(words[:count])
            multiwordIpa = self.getIpaFromLibrary(multiWord)
            if multiwordIpa is not None:
                return count, multiwordIpa, multiWord
        return 0, None, ""

    def transformWordToIpa(self, word:str):
        completeIpaLeft = ''
        completeIpaRight = ''
        completeWordLeft = []
        completeWordRight = []
        while word != '':
            remainingWordFirst, ipaFirst, firstPart = self.findFirstPartInWord(word)
            remainingWordLast, ipaLast, lastPart = self.findLastPartInWord(word)
            if len(remainingWordLast) < len(remainingWordFirst):
                completeIpaLeft = ipaLast + completeIpaLeft
                completeWordLeft.insert(0,lastPart)
                word = remainingWordLast
            else:
                completeIpaRight = completeIpaRight + ipaFirst
                completeWordRight.append(firstPart)                
                word = remainingWordFirst
        completeIpa = completeIpaRight + completeIpaLeft
        completeWordRight.extend(completeWordLeft)
        completeWords = '|'.join(completeWordRight)
        return completeIpa, completeWords


    def findFirstPartInWord(self, word:str):
        for wordPart in range(len(word), 0, -1):
            part = word[:wordPart]
            ipa = self.getIpaFromLibrary(part)
            if ipa is not None:
                remainingWord = word[wordPart:]
                return remainingWord, ipa, part
        raise Error('we have no match for single char in library with char: ' + word[0] + 'with full text:' + word)# pragma: no cover

    def findLastPartInWord(self, word:str):
        for wordPart in range(0,len(word)):
            part = word[wordPart:]
            ipa = self.getIpaFromLibrary(part)
            if ipa is not None:
                remainingWord = word[:wordPart]
                return remainingWord, ipa, part
        raise Error('we have no match for single char in library with char: ' + word[-1])# pragma: no cover

    def getIpaFromLibrary(self, word:str):
        ipa = self.getIpaFromLibraryExcactString(word)
        if ipa is  None:
            word = word.lower()
            ipa = self.getIpaFromLibraryExcactString(word)
        return ipa
    
    def getIpaFromLibraryExcactString(self,word:str):
        if word in self.library.index:
            ipa: str
            ipa = self.library.loc[word].values[0]
            if type(ipa) is not str:
                ipa = ipa[0]
            return ipa
        return None

    def removeEmphasis(self, text: str):
        if self.useEmphasis:
            return text
        withoutEmphasis = text.replace("ˈ","")
        return withoutEmphasis
        