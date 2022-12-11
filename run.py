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


class Extractor:
    def __init__(self, baseDomain):
        try:
            # Initializing important vars
            self.baseDomain = baseDomain
            self.tesseractPath = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            self.session = requests.Session()
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            pytesseract.pytesseract.tesseract_cmd = self.tesseractPath
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
            return captcha_code
        except:
            print("Error occured while decoding captcha!")

    def parseIndexPage(self, indexUrl):
        try:
            # Fetching index page [where you enter USN]
            indexUrl = urljoin(self.baseDomain, indexUrl)
            indexPage = self.session.get(
                indexUrl, headers=self.headers, verify=False)
            soup = BeautifulSoup(indexPage.content, "html.parser")
            # Setting important values
            self.img_src = soup.find(alt="CAPTCHA code")['src']
            self.token = soup.find('input')['value']
        except:
            print("Error while parsing Index page!")
