import os
from datetime import date


class File:

    def __init__(self, sem, reval, folderName):
        self.path = os.path.join(os.getcwd(), folderName)
        if not reval:
            self.name = f"{str(date.today())}-reg-{sem}"
        else:
            self.name = f"{str(date.today())}-reval-{sem}"

    def addData(self)
