import requests
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image as pimg
from wand.image import Image as wimg
import numpy
import io
import re


path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = path_to_tesseract

s = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

z = s.get("https://results.vtu.ac.in/JJEcbcs22/index.php",
          headers=headers, verify=False)

soup = BeautifulSoup(z.content, "html.parser")
img_src = soup.find(alt="CAPTCHA code")['src']
token = soup.find('input')['value']
p = s.get(f'https://results.vtu.ac.in/{img_src}', headers=headers, verify=False)
pic = wimg(blob=p.content)
pic.modulate(120)
pic.modulate(150)
pic.modulate(130)
img_buffer = numpy.asarray(
    bytearray(pic.make_blob(format='png')), dtype='uint8')
bytesio = io.BytesIO(img_buffer)
pil_img = pimg.open(bytesio)
captcha_code = re.sub('[\W_]+', '', pytesseract.image_to_string(pil_img))
pil_img.show()

m = s.post('https://results.vtu.ac.in/JJEcbcs22/resultpage.php',
           data={'Token': token, 'lns': '1cr20cs168', 'captchacode': captcha_code}, headers=headers, verify=False)


with open('reg.html', 'w', encoding='utf-8') as o:
    o.write(m.text)
