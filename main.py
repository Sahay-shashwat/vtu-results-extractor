from bs4 import BeautifulSoup

z = ''
with open('reg.html', 'r', encoding='utf-8') as f:
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
    for sem in tables[i].find_all('b'):
        print(sem.text)
        marksTable = sem.parent.find_next_sibling()
        tableRow = marksTable.find_all('div', {'class': 'divTableRow'})
        for row in range(1, len(tableRow)):
            for cell in tableRow[row].find_all('div', {'class': 'divTableCell'}):
                print(cell.text.strip())
