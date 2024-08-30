from flask import Flask, request, render_template, redirect, url_for, session, flash ,send_from_directory
import psycopg2
from psycopg2 import OperationalError, IntegrityError
from datetime import datetime, timezone,timedelta
from werkzeug.utils import secure_filename
import pandas as pd
import os
import datetime
from persiantools.jdatetime import JalaliDateTime



app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['vekalatname'] = "C:\\documents\\vekalatname"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)


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
            session.permanent = True
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
                current_timestamp = JalaliDateTime.now().to_gregorian()
                variz_mablagh = request.form['variz_mablagh']
                paziresh_number = request.form['paziresh_number']
                hesabe_varizi = request.form['hesabe_varizi']

                if mablagh_havaleh == '':
                    mablagh_havaleh = None
                if variz_mablagh == '':
                    variz_mablagh = None

                Final_mablagh = int(variz_mablagh) + int(mablagh_havaleh)

                if Final_mablagh == '':
                    Final_mablagh = None

                    
                cursor.execute("""
                    INSERT INTO first_info ("Car_type", "hesabe_varizi", "paziresh_number", "Darkhast_number", "Rabet_Name", "Rabet_Phone", "Mablagh_Havaleh(toman)", "Havale_City", "Havaleh_Owner_Name", "Havaleh_Owner_MelliCode", "Sakha_Password" , "inserted_date", "variz_mablagh", "final_mablagh")
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s)
                """, (car_type, hesabe_varizi, paziresh_number, darkhast_number, rabet_name, rabet_phone, mablagh_havaleh, havale_city, havaleh_owner_name, havaleh_owner_mellicode, sakha_password, current_timestamp, variz_mablagh, Final_mablagh))
                conn.commit()
                cursor.execute("""MERGE INTO tahvil_info AS target
                    USING (
                        SELECT DISTINCT "Darkhast_number", "paziresh_number"
                        FROM first_info
                        where "first_info"."Darkhast_number" != '' or "first_info"."paziresh_number" != ''
                    ) AS source
                    ON "target"."darkhast_number" = "source"."Darkhast_number"
                    AND "target"."paziresh_number" = "source"."paziresh_number"
                    WHEN NOT MATCHED THEN
                        INSERT ("darkhast_number", "paziresh_number", "shasi_number", "pelak_number", "parking_name", "tahvil_driver")
                        VALUES ("source"."Darkhast_number", "source"."paziresh_number", '', '', '', '')"""
                )
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
    if 'loggedin' in session:
        return render_template('search_complete.html')
    return redirect(url_for('login'))

@app.route('/first_info/search_complete/search_result', methods=['GET', 'POST'])
def search():
    if 'loggedin' in session:
        melli_code = request.form.get('melli_code')
        rabet_phone = request.form.get('rabet_phone')

        
        if melli_code and rabet_phone:
            cursor.execute("""SELECT * FROM first_info WHERE "Havaleh_Owner_MelliCode" = %s OR "Rabet_Phone" = %s ORDER BY "inserted_date"  DESC""", (melli_code, rabet_phone))
        elif melli_code:
            cursor.execute("""SELECT * FROM first_info WHERE "Havaleh_Owner_MelliCode" = %s ORDER BY "inserted_date"  DESC""", (melli_code,))
        elif rabet_phone:
            cursor.execute("""SELECT * FROM first_info WHERE "Rabet_Phone" = %s ORDER BY "inserted_date"  DESC""", (rabet_phone,))
        elif melli_code == '' and rabet_phone =='':
            cursor.execute("""SELECT * FROM first_info ORDER BY "inserted_date"  DESC """)
        
        results = cursor.fetchall()
        return render_template('search_results.html', results=results)
    return redirect(url_for('login'))

@app.route('/first_info/search_complete/update_record', methods=['GET', 'POST'])
def update_record():
    if 'loggedin' in session:
        Rabet_Phone = request.form.get('Rabet_Phone')
        Havaleh_Owner_MelliCode = request.form.get('Havaleh_Owner_MelliCode')

        cursor.execute("""SELECT * FROM "first_info" WHERE "Rabet_Phone" = %s and "Havaleh_Owner_MelliCode" = %s""", (Rabet_Phone, Havaleh_Owner_MelliCode))
        record = cursor.fetchone()
        
        return render_template('update_record.html', record=record)
    return redirect(url_for('login'))

@app.route('/first_info/search_complete/save_update', methods=['POST'])
def save_update():
    if 'loggedin' in session:
        darkhast_number = request.form['darkhast_number']
        car_type = request.form.get('car_type')
        rabet_name = request.form.get('rabet_name')
        rabet_phone = request.form.get('rabet_phone')
        mablagh_havaleh = request.form.get('mablagh_havaleh')
        havale_city = request.form.get('havale_city')
        havaleh_owner_name = request.form.get('havaleh_owner_name')
        havaleh_owner_mellicode = request.form.get('havaleh_owner_mellicode')
        sakha_password = request.form.get('sakha_password')
        variz_mablagh = request.form.get('variz_mablagh')
        hesabe_varizi = request.form.get('hesabe_varizi')
        paziresh_number = request.form.get('paziresh_number')

        if variz_mablagh == '':
            variz_mablagh = 0

        if mablagh_havaleh == '':
            mablagh_havaleh = 0

        # if mablagh_havaleh == 0 and variz_mablagh == 0:
        #     Final_mablagh == 0
        # else:
        #     Final_mablagh = int(variz_mablagh) + int(mablagh_havaleh)


        Final_mablagh = int(variz_mablagh) + int(mablagh_havaleh)



        cursor.execute("""
            UPDATE first_info
            SET "Car_type" = %s, "hesabe_varizi"=%s, "Darkhast_number" = %s, paziresh_number = %s, "Rabet_Name" = %s, "Rabet_Phone" = %s, "Mablagh_Havaleh(toman)" = %s, "Havale_City" = %s, "Havaleh_Owner_Name" = %s, "Havaleh_Owner_MelliCode" = %s, "Sakha_Password" = %s , "variz_mablagh" = %s, "final_mablagh" = %s
            WHERE "Rabet_Phone" = %s and "Havaleh_Owner_MelliCode" = %s 
        """, (car_type, hesabe_varizi, darkhast_number, paziresh_number, rabet_name, rabet_phone, mablagh_havaleh, havale_city, havaleh_owner_name, havaleh_owner_mellicode, sakha_password, variz_mablagh, Final_mablagh, rabet_phone, havaleh_owner_mellicode))
        conn.commit()
        cursor.execute("""MERGE INTO tahvil_info AS target
                        USING (
                            SELECT DISTINCT "Darkhast_number", "paziresh_number"
                            FROM first_info
                            where "first_info"."Darkhast_number" != '' or "first_info"."paziresh_number" != ''
                        ) AS source
                        ON "target"."darkhast_number" = "source"."Darkhast_number"
                        AND "target"."paziresh_number" = "source"."paziresh_number"
                        WHEN NOT MATCHED THEN
                            INSERT ("darkhast_number", "paziresh_number", "shasi_number", "pelak_number", "parking_name", "tahvil_driver")
                            VALUES ("source"."Darkhast_number", "source"."paziresh_number", '', '', '', '')"""
                    )
        conn.commit()
        flash('Data updated successfully!', 'success')
        return redirect(url_for('first_info'))
    return redirect(url_for('login'))

@app.route('/upload_document_search')
def upload_document_search():
    if 'loggedin' in session:
        return render_template('upload_document_search.html')
    return redirect(url_for('login'))

@app.route('/upload_document_search_complete', methods=['GET', 'POST'])
def upload_document_search_complete():
    if 'loggedin' in session:
        melli_code = request.form.get('melli_code')
        rabet_phone = request.form.get('rabet_phone')

        
        if melli_code and rabet_phone:
            cursor.execute("""SELECT * FROM first_info WHERE "Havaleh_Owner_MelliCode" = %s OR "Rabet_Phone" = %s""", (melli_code, rabet_phone))
        elif melli_code:
            cursor.execute("""SELECT * FROM first_info WHERE "Havaleh_Owner_MelliCode" = %s""", (melli_code,))
        elif rabet_phone:
            cursor.execute("""SELECT * FROM first_info WHERE "Rabet_Phone" = %s""", (rabet_phone,))
        elif melli_code == '' and rabet_phone =='':
            cursor.execute("""SELECT * FROM first_info ORDER BY "inserted_date"  DESC """)
        
        record = cursor.fetchall()
        return render_template('upload_document_search_complete.html', record=record)
    return redirect(url_for('login'))

@app.route('/upload_page', methods=['GET', 'POST'])
def update_page():
    if 'loggedin' in session:
        if request.method == 'POST':
            Darkhast_number = request.form.get('Darkhast_number')
            paziresh_number = request.form.get('paziresh_number')

            cursor.execute("""SELECT * FROM "first_info" WHERE "Darkhast_number" = %s and "paziresh_number" = %s""", (Darkhast_number, paziresh_number))
            record = cursor.fetchone()

            if record:
                return render_template('upload_form.html', record=record)
            else:
                flash('Record not found', 'danger')
                return redirect(url_for('update_page'))
        return render_template('upload_form.html', record=None)
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST', 'get'])
def upload_file():
    if 'loggedin' in session:
        if 'vekalat_tahvil' in request.files:
            Darkhast_Number = request.form['Darkhast_number']
            Paziresh_Number = request.form['paziresh_number']
            vekalat_tahvil = request.files['vekalat_tahvil']
            file_extension = os.path.splitext(vekalat_tahvil.filename)[1]
            filename = secure_filename(vekalat_tahvil.filename)
            y = JalaliDateTime.now().to_gregorian()
            x = str(JalaliDateTime.now())

            filename = Darkhast_Number + '_vekalatname_' + x[:11] + file_extension
            # secure_filename = secure_filename(file.filename)
            # Here you should save the file
            vekalat_tahvil.save(os.path.join(app.config['vekalatname'], filename))
            cursor.execute("""INSERT INTO "first_step_docs" ("filename", "darkhast_number", "paziresh_number", "upload_date") VALUES ( %s, %s, %s, %s) ON CONFLICT ("darkhast_number", "paziresh_number") DO UPDATE SET "filename" = EXCLUDED."filename" , "upload_date" = EXCLUDED."upload_date" """, (filename, Darkhast_Number, Paziresh_Number, y))
            conn.commit()
            
            flash(f"File uploaded successfully", 'success')
            return render_template('upload_document_search.html')

        flash(f"No file uploaded", 'danger')
        return render_template('upload_form.html')
    return redirect(url_for('login'))

@app.route('/download', methods=['GET', 'POST'])
def download_file():
    if 'loggedin' in session:
        
        if request.method in ['GET','POST']:
            darkhast_number = request.form['Darkhast_number2']
            paziresh_number = request.form['paziresh_number2']


            cursor.execute("""
                SELECT filename FROM first_step_docs
                WHERE darkhast_number = %s AND paziresh_number = %s
            """, (darkhast_number, paziresh_number))
            result = cursor.fetchone()

            if result:
                filename = result[0]
                directory = r'C:\documents\vekalatname'
                return send_from_directory(directory, filename, as_attachment=True)
            else:
                flash(f"فایل برای این رکورد آپلود نشده است", 'danger')
                return render_template('upload_document_search.html')
        return render_template('download.html')
    return redirect(url_for('login'))

@app.route('/search_tahvil')
def search_tahvil():
    if 'loggedin' in session:
        return render_template('search_tahvil.html')
    return redirect(url_for('login'))

@app.route('/search_result_tahvil', methods=['GET', 'POST'])
def search_result_tahvil():
    if 'loggedin' in session:
        melli_code = request.form.get('melli_code')
        rabet_phone = request.form.get('rabet_phone')

        if melli_code and rabet_phone:
            cursor.execute("""SELECT c."Havaleh_Owner_MelliCode", c."Rabet_Phone", c."inserted_date", c."Darkhast_number", c."paziresh_number", s."shasi_number", s."pelak_number", s."parking_name", s."tahvil_date", s."tahvil_driver" , c."Car_type" from "first_info" c LEFT JOIN "tahvil_info" s ON c."Darkhast_number" = s."darkhast_number" AND c."paziresh_number" = s."paziresh_number" WHERE (c."Darkhast_number" != '' and c."paziresh_number" != '') and (c."Havaleh_Owner_MelliCode" = %s OR c."Rabet_Phone" = %s ) ORDER BY c."inserted_date"  DESC """, (melli_code, rabet_phone))
        elif melli_code:
            cursor.execute("""SELECT c."Havaleh_Owner_MelliCode", c."Rabet_Phone", c."inserted_date", c."Darkhast_number", c."paziresh_number", s."shasi_number", s."pelak_number", s."parking_name", s."tahvil_date", s."tahvil_driver" , c."Car_type" from "first_info" c LEFT JOIN "tahvil_info" s ON c."Darkhast_number" = s."darkhast_number" AND c."paziresh_number" = s."paziresh_number" WHERE (c."Darkhast_number" != '' and c."paziresh_number" != '') and c."Havaleh_Owner_MelliCode" = %s ORDER BY c."inserted_date"  DESC """, (melli_code,))
        elif rabet_phone:
            cursor.execute("""SELECT c."Havaleh_Owner_MelliCode", c."Rabet_Phone", c."inserted_date", c."Darkhast_number", c."paziresh_number", s."shasi_number", s."pelak_number", s."parking_name", s."tahvil_date", s."tahvil_driver" , c."Car_type" from "first_info" c LEFT JOIN "tahvil_info" s ON c."Darkhast_number" = s."darkhast_number" AND c."paziresh_number" = s."paziresh_number" WHERE (c."Darkhast_number" != '' and c."paziresh_number" != '') and c."Rabet_Phone" = %s ORDER BY c."inserted_date"  DESC """, (rabet_phone,))
        elif melli_code == '' and rabet_phone =='':
            cursor.execute("""SELECT c."Havaleh_Owner_MelliCode", c."Rabet_Phone", c."inserted_date", c."Darkhast_number", c."paziresh_number", s."shasi_number", s."pelak_number", s."parking_name", s."tahvil_date", s."tahvil_driver" , c."Car_type" from "first_info" c LEFT JOIN "tahvil_info" s ON c."Darkhast_number" = s."darkhast_number" AND c."paziresh_number" = s."paziresh_number" WHERE (c."Darkhast_number" != '' and c."paziresh_number" != '') ORDER BY c."inserted_date"  DESC """)
        
        results = cursor.fetchall()


        return render_template('search_result_tahvil.html', results=results)
    return redirect(url_for('login'))

@app.route('/update_tahvil_record', methods=['GET', 'POST'])
def update_tahvil_record():
    if 'loggedin' in session:
        Darkhast_number = request.form.get('Darkhast_number')
        paziresh_number = request.form.get('paziresh_number')

        cursor.execute("""SELECT c."inserted_date", c."Darkhast_number", c."paziresh_number", s."shasi_number", s."pelak_number", s."parking_name", s."tahvil_date", s."tahvil_driver" , c."Car_type" from "first_info" c LEFT JOIN "tahvil_info" s ON c."Darkhast_number" = s."darkhast_number" AND c."paziresh_number" = s."paziresh_number" WHERE c."Darkhast_number" = %s AND c."paziresh_number" = %s """, (Darkhast_number, paziresh_number))
        record = cursor.fetchone()
        
        return render_template('update_tahvil_record.html', record=record)
    return redirect(url_for('login'))

@app.route('/save_tahvil_update', methods=['POST'])
def save_tahvil_update():
    if 'loggedin' in session:
        car_type = request.form['car_type']
        tarikh_kharid = request.form.get('tarikh_kharid')
        paziresh_number = request.form.get('paziresh_number')
        darkhast_number = request.form.get('darkhast_number')
        shasi_number = request.form.get('shasi_number')
        pelak_number = request.form.get('pelak_number')
        parking_name = request.form.get('parking_name')
        tahvil_date = request.form.get('tahvil_date')
        tahvil_driver = request.form.get('tahvil_driver')

        # if variz_mablagh == '':
        #     variz_mablagh = 0

        # if mablagh_havaleh == '':
        #     mablagh_havaleh = 0



        cursor.execute("""
            UPDATE tahvil_info
            SET "shasi_number" = %s, "pelak_number"=%s, "parking_name" = %s, tahvil_date = %s, "tahvil_driver" = %s
            WHERE "darkhast_number" = %s and "paziresh_number" = %s 
        """, (shasi_number, pelak_number, parking_name, tahvil_date, tahvil_driver, darkhast_number, paziresh_number))
        conn.commit()
        flash('Data updated successfully!', 'success')
        return redirect(url_for('search_tahvil'))
    return redirect(url_for('login'))










if __name__ == '__main__':
    app.run(debug=True)
