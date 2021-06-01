import bs4 as bs
import pandas as pd
from huiAudioCorpus.utils.PathUtil import PathUtil
import requests
import json
from tqdm import tqdm
from joblib import Parallel, delayed

class AudiosFromLibrivoxPersistenz:

    def __init__ (self, bookName: str, savePath: str, chapterPath: str, url:str = 'https://librivox.org/'):
        self.bookName = bookName
        self.url = url
        self.savePath = savePath
        self.chapterPath = chapterPath
        self.pathUtil = PathUtil()
        self.limitChapters = 1000
        self.rangeCapters = 20

    def save(self):
        chapters, chapterDownloadLinks = self.getChapter(self.bookName)
        Parallel(n_jobs=-2)(delayed(self.pathUtil.copyFileFromUrl)(link ,self.savePath+ '/' + link.split('/')[-1]) for link in chapterDownloadLinks)
        chapters.to_csv(self.chapterPath)
        

    def getChapter(self, bookName:str):
        searchUrl = self.getSearchUrl(bookName, self.url)
        response = self.loadSearchBook(searchUrl)
        chapterUrl = self.extractChapterUrl(response)
        chapterDownloadLinks = self.getChapterLinks(chapterUrl)
        chapters = pd.read_html(chapterUrl)
        return chapters[0], chapterDownloadLinks

    def loadSearchBook(self, url:str ):
        searchResult = requests.get(url)
        return searchResult.text

    def getSearchUrl(self, bookName: str, url:str):
        searchUrl = url + 'api/feed/audiobooks/?format=json&title=' + bookName 
        return searchUrl

    def extractChapterUrl(self, response: str):
        jsonInput = json.loads(response)['books']
        book = jsonInput[0]
        urlZipFile = book['url_librivox']
        return urlZipFile

    def extractZipUrl(self, response: str):
        jsonInput = json.loads(response)['books']
        book = jsonInput[0]
        urlZipFile = book['url_zip_file']
        return urlZipFile

    def getChapterLinks(self, url: str):
        searchResult = requests.get(url)
        searchResult.encoding = "UTF-8"
        soup = bs.BeautifulSoup(searchResult.text, 'html.parser')
        parsed_table = soup.find_all('table')[0] 
        data = [[td.a['href'] if td.find('a') else 
                ''.join(td.stripped_strings)
                for td in row.find_all('td')]
                for row in parsed_table.find_all('tr')]
        downloadLinks = [chapter[1] for chapter in data if len(chapter)>0]
        return downloadLinks


    def getIds(self):
        books = []
        limit = self.limitChapters
        for i in tqdm(range(self.rangeCapters)):
            requestUrl = f'https://librivox.org/api/feed/audiobooks/?format=json&limit={limit}&offset={i*limit}'
            page = requests.get(requestUrl)
            page.encoding = "UTF-8"
            result=  json.loads(page.text)
            if 'books' in result:
                books.extend(result['books'])
            else:
                print(result)
                break
        return books