

from flask import Flask, render_template, request, redirect, url_for, session

from flask_mysqldb import MySQL
import MySQLdb.cursors


# Files for random number
import random

# Files for generate qr
import qrcode



import pyzbar.pyzbar as pyzbar
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2



value = random.random()



app = Flask(__name__)
app.secret_key = 'sdkjdsfkbds3423'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'


mysql = MySQL(app)


@app.route('/',methods=['GET', 'POST'])
def login():


        if  request.method == 'POST':

            password = request.form['password']
            email = request.form['email']
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))

            account = cursor.fetchone()

            permission = account[5]
            print(permission)

            imp = (permission == 'done')

            ddata = email







            if account is None:
                return "something went wrong / invalid credentials"
            else:
                if imp is True:
                    pdata = 'You can go'
                    return render_template('dashboard.html',tData=ddata, psdata = pdata)
                else:
                    pdata = 'You can not go'
                    return render_template('dashboard.html', tData=ddata, psdata=pdata)


        return render_template('login.html')



@app.route("/logout")
def logout():

    return redirect('/')



@app.route('/signup/',methods=['GET', 'POST'])
def signup():
    try:
        if request.method == "POST":
            users = request.form
            name = users['name']
            email = users['email']
            password = users['password']

            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5)
            data = (name)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill="black", back_color="white")
            img.save("static\qrs\%s.png"%(email))



            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users(name, email ,password ) VALUES (%s, %s,%s)", (name, email, password))
            mysql.connection.commit()
            cur.close()
            return redirect("/", code=302)
        else:
            return render_template('/signup.html')

    except Exception as e:
        print(("error :", str(Exception)))
        return render_template('signup.html')




@app.route('/dabbu/',methods=['GET', 'POST'])
def dabbu():


    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
                    help="path to output CSV file containing barcodes")
    args = vars(ap.parse_args())
    # print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    # csv = open(args["output"], "a")
    # found = set()
    while True:

        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        cv2.line(frame, (85, 50), (100, 50), (255, 255, 255), 2)

        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:

            # (x, y, w, h) = barcode.rect
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            barcodeData = barcode.data.decode("utf-8")
            # barcodeType = barcode.type


            print(barcodeData)
            pdata = barcodeData
            cango = "done"


            cursor = mysql.connection.cursor()

            cursor.execute('''
                        UPDATE flask.users

                        SET permission = %s                            

                        WHERE name = %s       
                        ''',(cango,pdata))

            mysql.connection.commit()

            if barcodeData is None:
                return render_template('dabbu.html')
            else:
                return render_template('dabbu.html', dabbud=pdata)





            # text = "{} ({})".format(barcodeData, barcodeType)
            # cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # return render_template('dabbu.html')



            # if barcodeData not in found:
            #     return "Barcode not found"


        # cv2.imshow("QR-Code Scanner", frame)
        # key = cv2.waitKey(1) & 0xFF
        #
        # if key == ord("q"):
        vs.stop()
        break


    # print("[INFO] cleaning up...")
    # csv.close()
    # cv2.destroyAllWindows()
    # vs.stop()
    return render_template('dabbu.html')


# this is working

    # cap = cv2.VideoCapture(0)
    # font = cv2.FONT_HERSHEY_PLAIN
    #
    # while True:
    #     _, frame = cap.read()
    #
    #     decodedObjects = pyzbar.decode(frame)
    #     for obj in decodedObjects:
    #         print(str(obj.data))
    #
    #
    #         sdata = str(obj.data)
    #         return render_template('dabbu.html', ssdata = sdata)
    #
    #
    #
    #         # cursor = mysql.connection.cursor()
    #         # cursor.execute('SELECT * FROM users WHERE name = %s', (str(obj.data)))
    #
    #     break
    #
    #     # datav = cv2.imshow("QR Scanner", frame)
    #     #
    #     # key = cv2.waitKey(1)
    #     # if key == 27:
    #     #     break
    #
    # cap.release()
    # # cv2.destroyAllWindows()
    #
    # return render_template('dabbu.html')





@app.route('/gate/',methods=['GET', 'POST'])
def gate():


    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
                    help="path to output CSV file containing barcodes")
    vs = VideoStream(src=0).start()

    while True:

        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        cv2.line(frame, (85, 50), (100, 50), (255, 255, 255), 2)

        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")

            print(barcodeData)
            pdata = barcodeData
            cango = "undone"

            cursor = mysql.connection.cursor()

            cursor.execute('''
                        UPDATE flask.users
                        SET permission = %s                      
                        WHERE name = %s       
                        ''',(cango,pdata))

            mysql.connection.commit()

            if barcodeData is None:
                return render_template('gate.html')
            else:
                return render_template('gate.html', gated=pdata)

        break

    vs.stop()
    return render_template('gate.html')





@app.route('/interview/')
def interview():

    return render_template('interview.html')

@app.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')

if __name__=="__main__":
    app.run(debug=True)



