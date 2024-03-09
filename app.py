from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

app.secret_key = 'your_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Fungsi untuk membuat database
def create_database():
    with app.app_context():
        db.create_all()

# Panggil fungsi untuk membuat database
create_database()

# Rute untuk halaman login
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password. Please try again.'
    return render_template('login.html',error=error)

# Rute untuk halaman registrasi
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = 'Username already exists. Please choose another username.'
        elif password != confirm_password:
            error = 'Passwords do not match'
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('register.html', error=error)


# Rute untuk logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



def create_connection():
    conn = sqlite3.connect('database.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS items
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      quantity INTEGER NOT NULL,
                   description TEXT,
                   status TEXT
                   )''')
    conn.commit()
    conn.close()

create_table()

@app.route('/home')
def home():
    username = session.get('username') 
    if 'username' in session:
        return render_template('home.html', username=username)
    else:
        return redirect(url_for('login'))


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


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        description = request.form ['description']
        status = request.form['status']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO items (name, quantity, description, status) VALUES (?, ?, ?, ?)', (name, quantity, description, status))
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
        description = request.form ['description']
        status = request.form['status']
        cursor.execute('UPDATE items SET name=?, quantity=?, description=?, status=?, WHERE id=?', (name, quantity,description,status, id))
        conn.commit()
        conn.close()
        return redirect(url_for('show_items'))
    return render_template('update_item.html', item=item)

@app.route('/delete/<int:id>')
def delete_item(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('show_items'))

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
