import requests
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image as pimg
from wand.image import Image as wimg
import numpy
import io
import re


class Extractor:
    def __init__(self):
        try:
            self.tesseractPath = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            self.session = requests.Session()
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            pytesseract.pytesseract.tesseract_cmd = self.tesseractPath
        except:
            print("Error while initializing extractor!")

    def decodeCaptcha(self, blob):
        pass

    def parseIndexPage(self, url):
        try:
            indexPage = self.session.get(
                url, headers=self.headers, verify=False)
            soup = BeautifulSoup(indexPage.content, "html.parser")
            self.img_src = soup.find(alt="CAPTCHA code")['src']
            self.token = soup.find('input')['value']
        except:
            print("Error while parsing Index page!")
