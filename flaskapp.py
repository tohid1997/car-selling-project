from flask import Flask, request, render_template, redirect, url_for, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
conn = psycopg2.connect(
    dbname="WEBAPP",
    user="postgres",
    password="@Tohid221057",
    host="localhost"
)
cursor = conn.cursor()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'loggedin' in session and session['username'] == 'tohid':
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            return redirect(url_for('home'))
        return render_template('register.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['username'] = user[1]
            return redirect(url_for('home'))
        else:
            return "Incorrect username or password!"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
