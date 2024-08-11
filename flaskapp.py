from flask import Flask, request, render_template, redirect, url_for, session, flash
import psycopg2
from psycopg2 import OperationalError, IntegrityError

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
try:
    conn = psycopg2.connect(
        dbname="WEBAPP",
        user="postgres",
        password="@Tohid221057",
        host="localhost"
    )
    cursor = conn.cursor()
except OperationalError as e:
    print(f"Error connecting to the database: {e}")
    # Handle the error (e.g., log it, notify admin, etc.)
@app.route('/')
def route():
    if 'loggedin' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

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
            error = "نام کاربری یا رمز عبور شما اشتباه است!"
            return render_template('login.html', error = error)

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

@app.route('/first_info')
def first_info():
    if 'loggedin' in session:
        return render_template('first_info.html')
    return redirect(url_for('login'))

@app.route('/first_info/new_info', methods=['GET', 'POST'])
def first_info_new_info():
    if 'loggedin' in session:
        if request.method == 'POST':
            try:
                car_type = request.form['car_type']
                darkhast_number = request.form['darkhast_number']
                rabet_name = request.form['rabet_name']
                rabet_phone = request.form['rabet_phone']
                mablagh_havaleh = request.form['mablagh_havaleh']
                havale_city = request.form['havale_city']
                havaleh_owner_name = request.form['havaleh_owner_name']
                havaleh_owner_mellicode = request.form['havaleh_owner_mellicode']
                sakha_password = request.form['sakha_password']
                
                cursor.execute("""
                    INSERT INTO first_info ("Car_type", "Darkhast_number", "Rabet_Name", "Rabet_Phone", "Mablagh_Havaleh(toman)", "Havale_City", "Havaleh_Owner_Name", "Havaleh_Owner_MelliCode", "Sakha_Password")
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (car_type, darkhast_number, rabet_name, rabet_phone, mablagh_havaleh, havale_city, havaleh_owner_name, havaleh_owner_mellicode, sakha_password))
                conn.commit()
                flash('Data inserted successfully!', 'success')
            except IntegrityError:
                conn.rollback()
                flash("شماره درخواست تکراری است", 'danger')
            except Exception as e:
                conn.rollback()
                flash(f"An error occurred: {e}", 'danger')
            return redirect(url_for('first_info_new_info'))
        return render_template('first_info_new_info.html')
    return redirect(url_for('login'))


@app.route('/first_info/search_complete')
def index():
    return render_template('search_complete.html')



@app.route('/first_info/search_complete/search_result', methods=['GET', 'POST'])
def search():
    melli_code = request.form.get('melli_code')
    rabet_phone = request.form.get('rabet_phone')

    
    if melli_code and rabet_phone:
        cursor.execute("""SELECT * FROM first_info WHERE "Havaleh_Owner_MelliCode" = %s OR "Rabet_Phone" = %s""", (melli_code, rabet_phone))
    elif melli_code:
        cursor.execute("""SELECT * FROM first_info WHERE "Havaleh_Owner_MelliCode" = %s""", (melli_code,))
    elif rabet_phone:
        cursor.execute("""SELECT * FROM first_info WHERE "Rabet_Phone" = %s""", (rabet_phone,))
    
    results = cursor.fetchall()
    return render_template('search_results.html', results=results)




if __name__ == '__main__':
    app.run(debug=True)
