from flask import Flask, render_template,request 
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
   
    # cursor = conn.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)")
    return conn

# connection()





@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    name = request.form['username']
    email = request.form['email']
    password = request.form['password']

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (name, email, password))
    
    cursor = conn.cursor()          
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall() 
    cursor.close()
    conn.commit()
    print(users[1])
    return render_template('dashboard.html', users=users)

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    conn = connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        cursor.execute("UPDATE users SET username=?, email=?, password=? WHERE id=?", (username, email, password, user_id))
        conn.commit()
        cursor.execute("SELECT * FROM users")
        return render_template('dashboard.html', users=cursor.fetchall())
    
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    return render_template('edit_user.html', user=user)

@app.route('/delete/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    conn = connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    
    cursor.execute("SELECT * FROM users")
    
    return render_template('dashboard.html', users = cursor.fetchall())

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('userRegistration.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
