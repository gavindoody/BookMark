from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    sort_by = request.args.get('sort_by', 'title')
    filter_by = request.args.get('filter_by', '')

    query = 'SELECT * FROM books'
    params = []
    
    if filter_by:
        query += ' WHERE status = ?'
        params.append(filter_by)
    
    query += f' ORDER BY {sort_by}'
    
    books = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    status = request.form['status']
    pages_read = request.form.get('pages_read', 0)
    total_pages = request.form['total_pages']
    
    conn = get_db_connection()
    conn.execute("INSERT INTO books (title, author, status, pages_read, total_pages) VALUES (?, ?, ?, ?, ?)",
                 (title, author, status, pages_read, total_pages))
    conn.commit()
    conn.close()
    
    return redirect('/')

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        status = request.form['status']
        pages_read = request.form.get('pages_read', 0)
        total_pages = request.form['total_pages']
        
        conn.execute('UPDATE books SET title = ?, author = ?, status = ?, pages_read = ?, total_pages = ? WHERE id = ?',
                     (title, author, status, pages_read, total_pages, book_id))
        conn.commit()
        conn.close()
        
        return redirect('/')
    
    conn.close()
    return render_template('edit.html', book=book)

@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
