
from huiAudioCorpus.utils.PathUtil import PathUtil
from typing import Dict, List
from huiAudioCorpus.utils.DoneMarker import DoneMarker
from normalizer.normalizer import Normalizer

import re
import json

class Step3_1_PrepareText:

    def __init__(self, savePath: str, loadFile: str, saveFile: str, startSentence: str, endSentence: str, textReplacement: Dict[str,str],  normalizer: Normalizer, moves: List[Dict[str, str]], remove: List[Dict[str, str] ]):
        self.savePath = savePath
        self.normalizer = normalizer
        self.loadFile = loadFile
        self.saveFile = saveFile
        self.textReplacement = textReplacement
        self.pathUtil = PathUtil()
        self.startSentence = startSentence
        self.endSentence = endSentence
        self.moves = moves
        self.removes = remove

    def run(self):
        return DoneMarker(self.savePath).run(self.script)
    
    def script(self):
        inputText = self.pathUtil.loadFile(self.loadFile)
        cuttedText = self.cutText(inputText, self.startSentence , self.endSentence)
        removedText = self.remove(cuttedText, self.removes)
        replacedText = self.replace(removedText, self.textReplacement)
        movedText = self.move(replacedText, self.moves)
        self.pathUtil.writeFile(movedText, self.saveFile)

    def move(self, text: str, moves: List[Dict[str, str]]):
        for move in moves:
            start = move['start']
            end = move['end']
            after = move['after']
            textToMove = text.partition(start)[-1].partition(end)[0] + end
            textWithoutMove = text.replace(textToMove, "")
            first, seperator, last = textWithoutMove.partition(after)
            finalText = first + seperator + textToMove + last
            text = finalText
        return text

    def remove(self, text: str, removes: List[Dict[str, str]]):
        for remove in removes:
            textToRemove = ""
            textToRemove_old = None
            start = remove['start']
            end = remove['end']
            while textToRemove != textToRemove_old:
                textToRemvoe = start + text.partition(start)[-1].partition(end)[0] + end     
                text = text.replace(textToRemvoe, "")
                textToRemove_old = textToRemove
                print(textToRemvoe)
        return text


    def cutText(self, text: str, startSentence: str, endSentence: str):
        if startSentence =="":
            withoutFirst = text
        else:
            withoutFirst = startSentence + text.split(startSentence, 1)[1]
        
        if endSentence=="":
            withoutEnd = withoutFirst
        else:
            withoutEnd = withoutFirst.split(endSentence,1)[0] + endSentence
        
        stripped = withoutEnd.strip()
        prepared = stripped.replace('\r', '')
        return prepared

    def replace(self, text: str, textReplacement: Dict[str,str]):
        beforeReplacement = {
            '\xa0': ' '
        }
        baseReplacement =  {
            '...': '.',
            '«': ' ',
            '»': ' ',
            "'": '',
            '"': ' ',
            '_': ' ',
            '-': ' ',
            '–': ' ',
            ';': ',',
            ':': ':',
            '’': ' ',
            '‘': ' ',
            '<': ' ',
            '>': ' ',
            '(': ' ',
            ')': ' ',
            '›': ' ',
            '‹': ' ',
            'é': 'e',
            'ê': 'e',
            '^': ' ',
            'è': 'e',
            'à': 'a',
            'á': 'a'

        }
        
        abbreviations = {
            ' H. v.': ' Herr von ',
            '†': ' gestorben ',
            ' v.': ' von ',
            '§': ' Paragraph ',
            ' geb.': ' geboren ',
            ' u.': ' und ',
            '&': ' und ',
            ' o.': ' oder ',
            ' Nr.': ' Nummer ',
            ' Pf.': ' Pfennig ',
            ' Mk.': ' Mark ',
            " Sr. Exz.": " seiner exzellenz ",
            " Kgl.": " königlich ",
            " Dr.": ' Doktor ',
            ' Abb.': ' Abbildung ',
            ' Abh.': ' Abhandlung ',
            ' Abk.': ' Abkürzung ',
            ' allg.': ' allgemein ',
            ' bes.': ' besonders ',
            ' bzw.': ' beziehungsweise ',
            ' geb.': ' geboren ',
            ' gegr.': ' gegründet ',
            ' jmd.': ' jemand ',
            ' o. Ä.': ' oder Ähnliches ',
            ' u. a.': ' unter anderem ',
            ' o.Ä.': ' oder Ähnliches ',
            ' u.a.': ' unter anderem ',
            ' ugs.': ' umgangssprachlich ',
            ' urspr.': ' ursprünglich ',
            ' usw.': '  und so weiter',
            ' u. s. w.': ' und so weiter ',
            ' u.s.w.': ' und so weiter ',
            ' zz.': ' zurzeit ',
            ' dt.': '  deutsch',
            ' ev.': ' evangelisch ',
            ' Jh.': ' Jahrhundert ',
            ' kath.': ' katholisch ',
            ' lat.': ' lateinisch ',
            ' luth.': ' lutherisch ',
            ' Myth.': ' Mythologie ',
            ' natsoz.': ' nationalsozialistisch ',
            ' n.Chr.': ' nach Christus ',
            ' n. Chr.': ' nach Christus ',
            ' relig.': ' religiös ',
            ' v. Chr.': ' vor Christus ',
            ' v.Chr.': ' vor Christus ',
            ' Med.': ' Medizin ',
            ' Mio.': ' Millionen ',
            ' d.h.': ' das heißt ',
            ' d. h.': ' das heißt ',
            ' Abb.': ' Abbildung ',
            ' f.': ' folgende ',
            ' ff.': ' folgende ',
            ' ggf.': ' gegebenfalls ',
            ' i. Allg.': ' im Allgemeinen ',
            ' i. d. R.': ' in der Regel ',
            ' i.Allg.': ' im Allgemeinen ',
            ' i.d.R.': ' in der Regel ',
            ' lt.': ' laut ',
            ' m.': ' mit ',
            ' od.': ' oder ',
            ' s. o.': ' siehe oben ',
            ' s. u.': ' siehe unten ',
            ' s.o.': ' siehe oben ',
            ' s.u.': ' siehe unten ',
            ' Std.': ' Stunde ',
            ' tägl.': ' täglich ',
            ' Tsd.': ' Tausend ',
            ' tsd.': ' tausend ',
            ' v.': ' von ',
            ' z. B.': ' zum Beispiel ',
            ' z.B.': ' zum Beispiel ',
            ' Z. B.': ' zum Beispiel ',
            ' Z.B.': ' zum Beispiel ',
            ' Bsp.': ' Beispiel ',
            ' bzgl.': ' bezüglich ',
            ' ca.': ' circa ',
            ' dgl.': ' dergleichen ',
            ' etc.': ' et cetera ',
            ' evtl.': ' eventuell ',
            ' z.T.': ' zum Teil ',
            ' z. T.': ' zum Teil ',
            ' zit.': ' zitiert ',
            ' zzgl.': ' zuzüglich ',
            ' H. ': ' Herr ',
            ' N. N.': ' so und so ',
            ' N.N.': ' so und so ',
            ' u.s.f.': ' und so fort',
            ' u. s. f.': ' und so fort',
            ' von Ew.': ' von euerer ',
            ' Se.': ' seine ',
            ' St.': ' Sankt ',
            ' inkl.': ' inklusive ',
            'U.S.A.': ' U S A ',
            ' d. J': 'des Jahres ',
            'G.m.b.H.': ' GmbH ',
            ' Mr.': ' Mister ',
            '°': ' Grad ',
            ' m. E.': ' meines Erachtens ',
            ' m.E.': ' meines Erachtens ',
            ' Ew.': ' Eure ',
            ' a.O.': ' an der Oder ',
            ' d.': ' der ',
            ' Ev.': ' Evangelium ',
            ' Sr.': ' seiner ',
            ' hl.': ' heilige ',
            ' Hr.': ' Herr ',
            'd.i.': ' das ist ',
            ' Aufl.': ' Auflage ',
            "A. d. Üb.":" Anmerkung der Übersetzerin ",
            " gest.": " gestorben "
    

            
        }
        for input, target in beforeReplacement.items():
            text = text.replace(input,target)
        for input, target in textReplacement.items():
            text = text.replace(input,target)
        for input, target in baseReplacement.items():
            text = text.replace(input,target)

        self.pathUtil.writeFile(text, self.saveFile)

        remainingNumbers = [s for s in text.split() if bool(re.search(r'\d', s))]
        if len(remainingNumbers)>0:
            print('there are remaining number inside the text')
            print(remainingNumbers)
            replacements = {}
            for text in remainingNumbers:
                replacements[text] = self.normalizer.normalize(text)
            replacements = dict(sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True))
            print(json.dumps(replacements, indent=4, ensure_ascii=False))

            raise Exception('there are remaining number inside the text')

        remainingAbbreviations = [ab for ab in abbreviations.keys() if ab in text]
        if len(remainingAbbreviations)>0:
            print('there are remaining abbreviations inside the text')
            print(remainingAbbreviations)
            replacements = {key: value for (key,value) in abbreviations.items() if key in remainingAbbreviations}
            replacements = dict(sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True))
            print(json.dumps(replacements, indent=4, ensure_ascii=False))
            raise Exception('there are remaining abbreviations inside the text')

        aToZ = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        possibleAbberviations = [' '+char+'.' for char in 'abcdefghijklmnopqrstuvwxyz' if ' '+char+'.' in text] + [' '+char+char2+'.' for char in aToZ for char2 in aToZ if ' '+char+char2+'.' in text]
        shortWorts = [' Co.', ' go.', ' Da.',' na.',' ab.', ' an.', ' da.', ' du.', ' er.', ' es.', ' ja.', ' so.', ' um.', ' zu.', ' Ja.', ' Ad.', ' je.', ' Es.', ' ob.', ' is.', ' tu.', ' Hm.', ' So.', ' wo.', ' ha.', ' he.', ' Du.', ' du.', ' Nu.', ' in.']
        possibleAbberviations = [ab for ab in possibleAbberviations if ab not in shortWorts]
        if len(possibleAbberviations)>0:
            print('there are remaining possible abberviations inside the text')
            print(possibleAbberviations)
            raise Exception('there are remaining possible abberviations inside the text')
        
        allowedChars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ äöüßÖÄÜ .,;?!:" \n'
        remaininNotAllowedChars = [char for char in text if char not in allowedChars]
        if len(remaininNotAllowedChars)>0:
            print('there are remaining chars inside the text')
            print(remaininNotAllowedChars)
            raise Exception('there are remaining chars inside the text')
        return text