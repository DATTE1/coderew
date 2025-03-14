from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'eksmoparsing.db'

def get_books_from_database():
    with sqlite3.connect(app.config['DATABASE']) as connec:
        curs = connec.cursor()
        curs.execute('''SELECT * FROM Eksmo''')
        books = curs.fetchall()
    return [{'id': row[0], 'title': row[1], 'link': row[2], 'author': row[3]} for row in books]

@app.route('/')
def index():
    order = request.args.get('order')
    books = get_books_from_database()
    if order == 'title.asc':
        books.sort(key=lambda x: x['title'])
    elif order == 'title.desc':
        books.sort(key=lambda x: x['title'], reverse=True)
    elif order == 'author.asc':
        books.sort(key=lambda x: x['author'])
    elif order == 'author.desc':
        books.sort(key=lambda x: x['author'], reverse=True)
    return render_template('index.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
