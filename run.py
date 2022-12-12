from operator import index
from enums import ExtractorEnums as Const
from extractor import Extractor
from file import File
import os
from datetime import date
from db import Database
import re
import eel
import time

eel.init('ui')


@eel.expose
def extract(usns, link, reval):
    try:
        skipped = []
        link = link.replace('https://', '').replace('http://', '')
        resultCode = link.split('/')[1]
        indexUrl = "/".join([Const.BASE_DOMAIN.value,
                            resultCode, Const.INDEX_FILE.value])
        resultUrl = "/".join([Const.BASE_DOMAIN.value,
                             resultCode, Const.RESULT_FILE.value])
        usnList = [usn.lower() for usn in usns.split(",")]
        extractorObj = Extractor(Const.BASE_DOMAIN.value,
                                 indexUrl, resultUrl)
        for usn in usnList:
            if re.match(r'\d[a-zA-z]{2}\d{2}[a-zA-z]{2}\d{3,}', usn):
                res = extractorObj.extract(usn.lower(), reval)
                eel.queue(usn)
                if res == False:
                    skipped.append(usn)
                else:
                    time.sleep(3)
            else:
                skipped.append(usn)
        return {"status": True, "len": len(usnList)-len(skipped), "skipped": skipped}
    except Exception as e:
        print("Error occured while running script for extraction!", e)
        return {"status": False}


@eel.expose
def generate(usns, reval):
    try:
        skipped = []
        db = Database(os.getcwd())
        usnList = [usn.lower() for usn in usns.split(",")]
        for usn in usnList:
            maxSem = db.findMaxSem(usn.lower(), reval)[0][0]
            # Can be none if USN doesn't exist
            if maxSem:
                for i in range(1, int(maxSem)+1):
                    fileObj = File(
                        i, reval, Const.OUTPUT_FOLDER_NAME.value)
                    fileObj.addData(db.getData(
                        usn.lower(), reval, i, str(date.today())))
            else:
                skipped.append(usn)
        return {"status": True, "len": len(usnList)-len(skipped), "skipped": skipped}

    except:
        print("Error occured while generating!")
        return {"status": False}


# eel.queue('1cr20cs111')
eel.start('index.html')
