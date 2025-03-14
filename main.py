import sqlite3
import requests
from bs4 import BeautifulSoup

def ImportParsed(id, booknames, booklinks, bookauthors):
    connec = sqlite3.connect('eksmoparsing.db')
    curs = connec.cursor()
    curs.execute('SELECT * FROM Eksmo WHERE id == ?', (id,))
    res = curs.fetchall()
    if not res:
        curs.execute('INSERT INTO Eksmo (id, [Книга], [Ссылка], [Автор]) VALUES(?, ?, ?, ?)', (id, booknames, booklinks, bookauthors))
    else:
        curs.execute('UPDATE Eksmo SET [Книга] = ?, [Ссылка] = ?, [Автор] = ? WHERE id = ?',(booknames, booklinks, bookauthors, id))
    connec.commit()
    connec.close()

connec = sqlite3.connect('eksmoparsing.db')
curs = connec.cursor()
curs.execute('''
            CREATE TABLE IF NOT EXISTS Eksmo 
            (id INTEGER PRIMARY KEY,
            [Книга] TEXT NOT NULL,
            [Ссылка] TEXT NOT NULL,
            [Автор] TEXT NOT NULL)
            ''')

id = -1
for i in range(1,50):
    url = 'https://eksmo.ru/comics_adult/' + f'page{i}/'
    page = requests.get(url, timeout=7)
    soup = BeautifulSoup(page.text, 'html.parser')
    Content = soup.find_all('a', class_='book__link')
    for x in Content:
        id += 1
        bookname = x.find('div', class_='book__name')
        booklink = "https://eksmo.ru" + x.get('href')
        if x.find('div', class_='book__author') is not None:
            bookauthor = x.find('div', class_='book__author')
        else:
            souphelper = BeautifulSoup(requests.get(booklink, timeout=7).content, 'html.parser')
            # content определяет кодировку сайта, если с этим есть проблемы
            bookauthor = souphelper.find('div', class_='book-page__card-author')
#        print(bookname.text.strip(), " ", booklink, " ", str(bookauthor.text.strip()), "\n")
        if bookname is not None:
            ImportParsed(id, bookname.text.strip(), booklink, bookauthor.text.strip())
        bookname = None
        bookauthor = None
        booklink = None