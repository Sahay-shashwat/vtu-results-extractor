from enums import ExtractorEnums as Const
from extractor import Extractor
from file import File
import os
from datetime import date
from db import Database
import re
import eel
from requests.compat import urljoin

eel.init('ui')
skipped = []


@eel.expose
def extract(usns, link):
    try:
        resultCode = link.split('/')[1]
        indexUrl = urljoin(Const.BASE_DOMAIN.value,
                           resultCode, Const.INDEX_FILE.value)
        resultUrl = urljoin(Const.BASE_DOMAIN.value,
                            resultCode, Const.RESULT_FILE.value)
        usnList = [usn.lower() for usn in usns.split(",")]
        extractorObj = Extractor(Const.BASE_DOMAIN.value,
                                 indexUrl, resultUrl)
        for usn in usnList:
            if re.match(r'\d[a-zA-z]{2}\d{2}[a-zA-z]{2}\d{3,}', usn):
                # extractorObj.extract(usn.lower(), False)
                pass
            else:
                skipped.append(usn)
        return {"status": True, "len": len(usnList)-len(skipped), "skipped": skipped}
    except Exception as e:
        print("Error occured while running script for extraction!", e)
        return {"status": False}


@eel.expose
def generate(usns):
    db = Database(os.getcwd())
    for usn in usns:
        maxSem = db.findMaxSem(usn.lower(), False)[0][0]
        # Can be none if USN doesn't exist
        if maxSem:
            for i in range(1, int(maxSem)+1):
                fileObj = File(
                    i, False, Const.OUTPUT_FOLDER_NAME.value)
                fileObj.addData(db.getData(
                    usn.lower(), False, i, str(date.today())))
    else:
        skipped.append(usn)


eel.start('index.html')
