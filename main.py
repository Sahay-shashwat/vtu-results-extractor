from bs4 import BeautifulSoup
import xlsxwriter
import re
from db import Database
import os
import re

whitespaceRegEx = re.compile(r'\s+')
db = Database(os.getcwd())

workbook = xlsxwriter.Workbook('demo.xlsx')
worksheet = workbook.add_worksheet()

z = ''
with open('test_files/reg.html', 'r', encoding='utf-8') as f:
    z = f.read()

soup = BeautifulSoup(z, 'lxml')
soup.prettify()
tables = soup.find_all('div', {"class": "col-md-12 table-responsive"})

# Fetching Student Details
studentDetails = tables[0].table.find_all('b')
usn = studentDetails[1].next_sibling.strip()
name = studentDetails[3].next_sibling.strip()

# Iterating through every semester and fetching details for both reval and reg
for i in range(1, len(tables)):
    semester = tables[i].find_all('b')[0]
    sem = semester.get_text().replace('Semester : ', '')
    print(sem)
    marksTable = semester.parent.find_next_sibling()
    tableRow = marksTable.find_all('div', {'class': 'divTableRow'})
    excelCellNumber = 2
    for row in range(1, len(tableRow)):
        excelCellNumber += 1
        cells = tableRow[row].find_all('div', {'class': 'divTableCell'})
        cellData = [whitespaceRegEx.sub(
            " ", val.text.strip()).strip() for val in cells]

        db.insertRecord(False, usn, name, sem, *cellData)

workbook.close()
