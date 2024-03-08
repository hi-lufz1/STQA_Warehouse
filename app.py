from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'




def create_connection():
    conn = sqlite3.connect('database.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS items
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      quantity INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()
    
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE name LIKE ?", ('%' + search_query + '%',))
        items = cursor.fetchall()
        conn.close()
        return render_template('search_results.html', items=items)
    return render_template('search.html')


@app.route('/')
def index():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return render_template('index.html', items=items)


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO items (name, quantity) VALUES (?, ?)', (name, quantity))
        conn.commit()
        conn.close()
        return redirect(url_for('show_items'))
    return render_template('add_item.html')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE id=?', (id,))
    item = cursor.fetchone()
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        cursor.execute('UPDATE items SET name=?, quantity=? WHERE id=?', (name, quantity, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('update_item.html', item=item)


@app.route('/delete/<int:id>')
def delete_item(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/show')
def show_items():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return render_template('show_items.html', items=items)


if __name__ == '__main__':
    app.run(debug=True)
