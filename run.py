from email import header
from email.mime import base
import requests
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image as pimg
from wand.image import Image as wimg
import numpy
import io
import re
from urllib.parse import urljoin
from db import Database
import os
from requests.packages import urllib3


class Extractor:
    def __init__(self, baseDomain, indexUrl, resultUrl):
        try:
            # Initializing important vars
            self.baseDomain = baseDomain
            self.tesseractPath = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            self.session = requests.Session()
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            pytesseract.pytesseract.tesseract_cmd = self.tesseractPath
            self.indexUrl = urljoin(self.baseDomain, indexUrl)
            self.resultUrl = urljoin(self.baseDomain, resultUrl)
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            self.db = Database(os.getcwd())
        except:
            print("Error while initializing extractor!")

    def decodeCaptcha(self):
        try:
            # Fetching captcha image
            captchaUrl = urljoin(self.baseDomain, self.img_src)
            captchaPage = self.session.get(
                captchaUrl, headers=self.headers, verify=False)
            pic = wimg(blob=captchaPage.content)
            # Modifying Image to prepare for OCR
            pic.modulate(120)
            pic.modulate(150)
            pic.modulate(130)
            img_buffer = numpy.asarray(
                bytearray(pic.make_blob(format='png')), dtype='uint8')
            bytesio = io.BytesIO(img_buffer)
            # Performing OCR on image
            pil_img = pimg.open(bytesio)
            captcha_code = re.sub(
                '[\W_]+', '', pytesseract.image_to_string(pil_img))
            self.captchaCode = captcha_code
        except:
            print("Error occured while decoding captcha!")

    def parseIndexPage(self):
        try:
            # Fetching index page [where you enter USN]

            indexPage = self.session.get(
                self.indexUrl, headers=self.headers, verify=False)
            soup = BeautifulSoup(indexPage.content, "html.parser")
            # Setting important values
            self.img_src = soup.find(alt="CAPTCHA code")['src']
            self.token = soup.find('input')['value']
        except:
            print("Error while parsing Index page!")

    def parseResultPage(self, usn, reval):
        resultPage = self.session.post(self.resultUrl, data={
                                       'Token': self.token, 'lns': usn, 'captchacode': self.captchaCode}, headers=self.headers, verify=False)
        whitespaceRegEx = re.compile(r'\s+')
        try:
            # Making sure the result page is fetched
            if (len(resultPage.text) > 200):
                soup = BeautifulSoup(resultPage.text, 'html.parser')
                # Adding records to DB after parsing result page
                tables = soup.find_all(
                    'div', {"class": "col-md-12 table-responsive"})

                # Fetching Student Details
                studentDetails = tables[0].table.find_all('b')
                usn = studentDetails[1].next_sibling.strip()
                name = studentDetails[3].next_sibling.strip()

                # Iterating through every semester and fetching details for both reval and reg
                for i in range(1, len(tables)):
                    semester = tables[i].find_all('b')[0]
                    sem = semester.get_text().replace('Semester : ', '')
                    marksTable = semester.parent.find_next_sibling()
                    tableRow = marksTable.find_all(
                        'div', {'class': 'divTableRow'})
                    excelCellNumber = 2
                    for row in range(1, len(tableRow)):
                        excelCellNumber += 1
                        cells = tableRow[row].find_all(
                            'div', {'class': 'divTableCell'})
                        cellData = [whitespaceRegEx.sub(
                            " ", val.text.strip()).strip() for val in cells]
                        # Inserting detail into db
                        self.db.insertRecord(
                            reval, usn, name, sem, *cellData)
            else:
                # Retry if captcha is wrong else USN is invalid
                if(len(resultPage.text) < 130):
                    self.extract(usn, reval)
        except:
            print("Error occured while parsing result!")

    def extract(self, usn, reval):
        try:
            self.parseIndexPage()
            self.decodeCaptcha()
            self.parseResultPage(usn, reval)
        except Exception as e:
            print('Error occured while performing extraction!', e)
