from typing import List, Union
from huiAudioCorpus.utils.PathUtil import PathUtil
import re
from bs4 import BeautifulSoup
import requests
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers

class GutenbergBookPersistenz:

    def __init__(self, textId: Union[str,int], savePath: str):
        self.textId = textId
        self.savePath = savePath
        self.pathUtil = PathUtil()
        self.guttenbergProjektDownload = GuttenbergProjektDownload()
        self.guttenbergDownload = GuttenbergDownload()

    def save(self):
        if isinstance(self.textId, str) :
            text = self.guttenbergProjektDownload.downloadText(self.textId)
        else:
            text = self.guttenbergDownload.downloadText(self.textId)
        self.pathUtil.writeFile(text, self.savePath)


class GuttenbergProjektDownload():
    """
    This class downloads a book from www.projekt-gutenberg.org
    The id has to be searched manual with the link https://www.projekt-gutenberg.org/info/texte/allworka.html
    You have to use the last part of the links for example dauthend/biwasee/biwasee.html
    """

    def __init__(self):
        self.baseLink = 'https://www.projekt-gutenberg.org/'

    def getIds(self):
        works_link = self.baseLink + "info/texte/allworka.html"

        works = requests.get(works_link)
        works.encoding = "UTF-8"

        works_soup = BeautifulSoup(works.text,"html.parser")

        books = []
        lastName=''
        firstName=''
        elements = works_soup.find("dl")
        for element in elements:
            if element.name == 'dt':
                currentAuthor = element.text
                if ', ' in currentAuthor:
                        names = currentAuthor.split(', ')
                        firstName = names[-1]
                        lastName = names[0]

                else: 
                    lastName = currentAuthor,
                    firstName = ''

            if element.name == 'dd':
                link = element.find("a")
                if link is not None:
                    id = link["href"][5:]
                    bookname = link.text
                    books.append({
                        'name': bookname,
                        'fistName': firstName,
                        'lastName': lastName,
                        'id': id
                    })
        return books

    def downloadText(self, textId: str):
        link = self.baseLink + textId
        fullText = ''
        while link is not None:
            paragraph, link = self.downloadPage(link)
            preparedParagraph = self.prepareParagraph(paragraph)
            fullText+=preparedParagraph
        return fullText

    def downloadPage(self, link: str):
        page = requests.get(link)
        page.encoding = "UTF-8"
        pageSoup = BeautifulSoup(page.text,"html.parser")
        paragraphs = pageSoup.find('p').find_all("p")
        nextLink = None
        if len(pageSoup.find_all("a",text=re.compile("weiter\s*>>")))>0:

            directLink = pageSoup.find("a",text=re.compile("weiter\s*>>"))["href"]

            nextLink = page.url.split("/")

            nextLink.pop()

            nextLink.append(directLink)

            nextLink = "/".join(nextLink)
        
        return paragraphs, nextLink


    def prepareParagraph(self, paragraphs:List):
        extractedParagraphs = ''
        for paragraph in paragraphs:
            for footnote in paragraph.select('span'):
                footnote.extract()

            if len(paragraph.text) > 0:
                extractedParagraph = re.sub(r" +",r" ",paragraph.text.replace("\t"," ").replace("\n", " "))

                extractedParagraphs += extractedParagraph.strip()+"\n"
        return extractedParagraphs


class GuttenbergDownload:
    """
    This class downloads a book from www.projekt-gutenberg.org
    The id has to be searched manual with the link http://gutendex.com/books/?search=ThisIsTheSearchText
    """
    def downloadText(self, textId: int):
        text = strip_headers(load_etext(textId, mirror='http://eremita.di.uminho.pt/gutenberg/')).strip()
        return text

