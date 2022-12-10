from bs4 import BeautifulSoup
import xlsxwriter

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
name = studentDetails[1].next_sibling
usn = studentDetails[3].next_sibling
print(name.strip())
print(usn.strip())

# Iterating through every semester and fetching details
for i in range(1, len(tables)):
    semester = tables[i].find_all('b')[0]
    sem = semester.get_text().replace('Semester : ', '')
    print(sem)
    marksTable = semester.parent.find_next_sibling()
    tableRow = marksTable.find_all('div', {'class': 'divTableRow'})
    for row in range(1, len(tableRow)):
        cells = tableRow[row].find_all('div', {'class': 'divTableCell'})
        for k in range(len(cells)):
            worksheet.write(0, k, cells[k].text.strip())
            # print(cell.text.strip())
workbook.close()