

from ttsCode.src.utils.PathUtil import PathUtil
from ttsCode.src.persistenz.AudiosFromLibrivoxPersistenz import AudiosFromLibrivoxPersistenz
from ttsCode.src.utils.DoneMarker import DoneMarker
from tqdm import tqdm

class Step0_Overview:

    def __init__(self, audiosFromLibrivoxPersistenz: AudiosFromLibrivoxPersistenz, savePath: str, pathUtil: PathUtil):
        self.savePath = savePath
        self.audiosFromLibrivoxPersistenz = audiosFromLibrivoxPersistenz
        self.pathUtil = pathUtil

    def run(self):
        return DoneMarker(self.savePath).run(self.script, deleteFolder=False)
    
    def script(self):
        booksLibrivox = self.downloadOverviewLibrivox()
        usableBooks = self.downloadChapters(booksLibrivox)
        speackerOverview = self.generateSpeackerOverview(usableBooks)
        speackerShort = self.generateSpeackerShort(speackerOverview)
        self.generateSpeackerTemplate(usableBooks)

        print('Usable books:', len(usableBooks))
        print('Total hours:',sum([book['time'] for book in usableBooks])/60/60)
        print('Count of Speackers:', len(speackerShort))
        print('bestSpeacker:', speackerShort[0])

    def downloadOverviewLibrivox(self):
        librivoxPath = self.savePath + '/booksLibrivox.json'
        if not self.pathUtil.fileExists(librivoxPath):
            print('Download Overview from Librivox')
            booksLibrivox  = self.audiosFromLibrivoxPersistenz.getIds()
            self.pathUtil.saveJson(librivoxPath, booksLibrivox)

        booksLibrivox = self.pathUtil.loadJson(librivoxPath)
        return booksLibrivox

    def downloadChapters(self, booksLibrivox):
        usableBookPath = self.savePath + '/usableBooks.json'
        if not self.pathUtil.fileExists(usableBookPath):
            print('Download Chapters from Librivox')
            usableBooks = [{'time': book['totaltimesecs'], 'title':book['title'], 'url': book['url_text_source']} for book in booksLibrivox if self.isBookUseable(book)]
            for book in tqdm(usableBooks):
                chapters, chapterDownloadLinks = self.audiosFromLibrivoxPersistenz.getChapter(book['title'])
                book['chapters'] = []
                for _, chapter in chapters.iterrows():
                    book['chapters'].append({
                        'title': chapter['Chapter'],
                        'reader': chapter['Reader'],
                        'time': convertToSeconds(chapter['Time'])
                    })
            self.pathUtil.saveJson(usableBookPath, usableBooks)

        usableBooks = self.pathUtil.loadJson(usableBookPath)
        return usableBooks

    def isBookUseable(self, book):
        if book['totaltimesecs']<=0:
            return False
        if book['language'] != "German":
            return False
        if 'www.projekt-gutenberg.org' in book['url_text_source']:
            return True

        if 'www.gutenberg.org/' in book['url_text_source']:
            return True
        return False

    def generateSpeackerTemplate(self, usableBooks):
        readerPath = self.savePath + '/readerTemplate.json'
        if not self.pathUtil.fileExists(readerPath):
            reader = {}
            for book in usableBooks:
                bookTitle = book['title']
                for chapter in book['chapters']:
                    if chapter['reader'] not in reader:
                        reader[chapter['reader']] = {}

                    title = ''.join([i for i in bookTitle.lower().replace(' ','_') if (i in 'abcdefghijklmonpqrstuvwxyz_' or i.isnumeric())])
                    guttenbergId = book['url'].replace('www.projekt-gutenberg.org/', '').replace('https://','').replace('http://','')
                    if 'www.gutenberg.org/' in guttenbergId:
                        guttenbergId = int(guttenbergId.replace('www.gutenberg.org/ebooks/', '').replace('www.gutenberg.org/etext/', ''))

                    reader[chapter['reader']][title] = {
                        'title': title,
                        'LibrivoxBookName': bookTitle,
                        'GutenbergId': guttenbergId,
                        'GutenbergStart': '',
                        'GutenbergEnd': '',
                        'textReplacement':{}
                    }



            self.pathUtil.saveJson(readerPath, reader)
        reader = self.pathUtil.loadJson(readerPath)
        return reader

    def generateSpeackerOverview(self, usableBooks):
        readerPath = self.savePath + '/readerLong.json'
        if not self.pathUtil.fileExists(readerPath):
            reader = {}
            for book in usableBooks:
                bookTitle = book['title']
                for chapter in book['chapters']:
                    if chapter['reader'] not in reader:
                        reader[chapter['reader']] = []

                    reader[chapter['reader']].append({
                        'title': chapter['title'],
                        'time': chapter['time'],
                        'book': bookTitle
                    })
            self.pathUtil.saveJson(readerPath, reader)
        reader = self.pathUtil.loadJson(readerPath)
        return reader

    def generateSpeackerShort(self, speackerOverview):
        readerPath = self.savePath + '/readerShort.json'
        if not self.pathUtil.fileExists(readerPath):
            readers = []
            for speacker in speackerOverview:
                readers.append({
                    'name': speacker,
                    'time': round(sum([chapter['time'] for chapter in speackerOverview[speacker]])/60/60,1)
                })
            readers.sort(key=lambda x: x['time'], reverse=True)
            self.pathUtil.saveJson(readerPath, readers)
        readers = self.pathUtil.loadJson(readerPath)
        return readers


def convertToSeconds(timeString: str):
    ftr = [3600,60,1]
    duration = sum([a*b for a,b in zip(ftr, map(int,timeString.split(':')))])
    return duration