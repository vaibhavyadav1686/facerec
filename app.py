from flask import Flask, render_template, request, redirect, url_for, session,Response
import mysql.connector as sqltr
import re
import cv2
import face_recognition
import numpy as np
import os

import pickle
import time






from time import time

class Camera(object):
    def __init__(self):
        self.frames = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

    def get_frame(self):
        return self.frames[int(time()) % 3]


def gen_frames():
    camera=cv2.VideoCapture(0)
    
    

            

            
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    

mycon=sqltr.connect(host="localhost",user="root",passwd="root",database="login")
 
app = Flask(__name__)
 
 
app.secret_key = 'your secret key'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'login'
 

 
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mycon.cursor()
        cursor.execute("SELECT * FROM account WHERE username = '%s' AND password = '%s'" %(username, password))
        account = cursor.fetchone()
        if account:
            
            return render_template('auth.html')
        else:
            mesg = 'Incorrect username / password !'
    return render_template('login.html', msg = mesg)

@app.route('/logout')
def logout():
    
    return redirect(url_for('login'))




@app.route('/video')
def video():
    return Response(gen_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam',methods=['GET', 'POST'])
def webcam():
    cursor = mycon.cursor()
    cursor.execute("SELECT images FROM account")
    x=cursor.fetchone()
    KNOWN_FACES_DIR=x[0]
    
    #KNOWN_FACES_DIR = r"C:\Users\hai\Desktop\FACEREC\LOGIN"

    TOLERANCE = 0.5
    FRAME_THICKNESS = 3
    FONT_THICKNESS = 2
    MODEL = 'hog'  # default: 'hog', other one can be 'cnn' - CUDA accelerated (if available) deep-learning pretrained model

    video = cv2.VideoCapture(0)



    def name_to_color(name):
        # Take 3 first letters, tolower()
        # lowercased character ord() value rage is 97 to 122, substract 97, multiply by 8
        color = [(ord(c.lower())-97)*8 for c in name[:3]]
        return color



    known_faces = []
    known_names = []




        # Next we load every file of faces of known person
    for filename in os.listdir(f'{KNOWN_FACES_DIR}'):

            # Load an image
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{filename}')

            # Get 128-dimension face encoding
            # Always returns a list of found faces, for this purpose we take first face only (assuming one face per image as you can't be twice on one image)
        encoding = face_recognition.face_encodings(image)[0]
        

            # Append encodings and name
            
        #encoding = pickle.load(open(f"C:/Users/hai/Desktop/FACEREC/LOGIN/{filename}","rb"))
        known_faces.append(encoding)
            
        




    # Now let's loop over a folder of faces we want to label
    while True:

        # Load image
        #print(f'Filename {filename}', end='')
        ret, image = video.read()

        # This time we first grab face locations - we'll need them to draw boxes
        locations = face_recognition.face_locations(image ,model=MODEL)

        # Now since we know loctions, we can pass them to face_encodings as second argument
        # Without that it will search for faces once again slowing down whole process
        encodings = face_recognition.face_encodings(image, locations)

        # We passed our image through face_locations and face_encodings, so we can modify it
        # First we need to convert it from RGB to BGR as we are going to work with cv2
        #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # But this time we assume that there might be more faces in an image - we can find faces of dirrerent people
        
        for face_encoding, face_location in zip(encodings, locations):

            # We use compare_faces (but might use face_distance as well)
            # Returns array of True/False values in order of passed known_faces
            results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)

            # Since order is being preserved, we check if any face was found then grab index
            # then label (name) of first matching known face withing a tolerance
           
            if True in results:
                if request.method=="POST":
                    return render_template('index.html')
            else:
                mesg = 'Authorization failed!'
            return render_template('login.html', msg = mesg)


@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=='GET':
        return render_template('add.html')
imcon=''
@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='GET':
        return render_template('protosearch.html')
@app.route('/image',methods=['GET','POST'])
def image():
    global imcon
    x=imcon
    return render_template('results_miss.html',x)
mycon2=sqltr.connect(host="localhost",user="root",passwd="root",database="record")
@app.route('/recognition',methods=['GET','POST'])
def recognition():
    if request.method=="POST":
        if request.form['img1'].endswith(".jpg"):
            cursor=mycon2.cursor()
            cursor.execute("SELECT images from arrested")
            arr=cursor.fetchall()
            cursor.execute("SELECT images from missing")
            miss=cursor.fetchall()
            cursor.execute("SELECT images from body")
            body=cursor.fetchall()
            
            

            KNOWN_FACES_DIR = [arr,body,miss]
            UNKNOWN_FACES_DIR = request.form["img1"]
            TOLERANCE = 0.6
            FRAME_THICKNESS = 3
            FONT_THICKNESS = 2
            MODEL = 'hog'
            known_faces = []
            known_names = []
            for record in KNOWN_FACES_DIR:
                for person in record:
                    x=(person[-1]).split(".jpg")
                    x.remove('')
                    for name in x:
                        name+=".jpg"
                        image = face_recognition.load_image_file(name)
                        
                        encoding = face_recognition.face_encodings(image)
                        
                        known_faces.append(encoding)
                        
                    image = face_recognition.load_image_file(UNKNOWN_FACES_DIR)

                    # This time we first grab face locations - we'll need them to draw boxes
                    locations = face_recognition.face_locations(image, model=MODEL)

                    # Now since we know loctions, we can pass them to face_encodings as second argument
                    # Without that it will search for faces once again slowing down whole process
                    encodings = face_recognition.face_encodings(image, locations)

                    # We passed our image through face_locations and face_encodings, so we can modify it
                    # First we need to convert it from RGB to BGR as we are going to work with cv2
                    

                    # But this time we assume that there might be more faces in an image - we can find faces of dirrerent people
                    
                    for face_encoding, face_location in zip(encodings, locations):

                        # We use compare_faces (but might use face_distance as well)
                        # Returns array of True/False values in order of passed known_faces
                        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)

                        # Since order is being preserved, we check if any face was found then grab index
                        # then label (name) of first matching known face withing a tolerance
                        
                        if np.count_nonzero(results)>3:
                            recog=x[0]+'.jpg'

                            
                            if recog in arr[0][-1]:
                                cursor.execute("select * from arrested where images='%s'"%(person[-1],))
                                d=cursor.fetchall()
                                d=d[0]
                                return render_template("results_arr.html",msg1=d[0],msg2=d[1],msg3=d[2],msg4=d[3],msg5=d[4],msg6=d[5])
                                        
                            if recog in miss[0][-1]:
                                cursor.execute("select * from missing where images='%s'"%(person[-1],))
                                d=cursor.fetchall()
                                d=d[0]
                                return render_template("results_miss.html",msg=imcon,msg1=d[0],msg2=d[1],msg3=d[2],msg4=d[3],msg5=d[4],msg6=d[5],msg7=d[6])


                                 
                            if recog in body[0][-1]:
                                cursor.execute("select * from body where images='%s'"%(person[-1],))
                                f=cursor.fetchall()
                                f=f[0]
                                return render_template("results_body.html",msg1=d[0],msg2=d[1],msg3=d[2],msg4=d[3])
            return render_template("protosearch.html",msg="Record Not Found!!!")
        
                    






            
            
        if request.form["img1"].endswith(".mp4"):
            cursor=mycon2.cursor()
            cursor.execute("SELECT images from arrested")
            arr=cursor.fetchall()
            cursor.execute("SELECT images from missing")
            miss=cursor.fetchall()
            cursor.execute("SELECT images from body")
            body=cursor.fetchall()
            
            

            KNOWN_FACES_DIR = [arr,miss,body]
            
            TOLERANCE = 0.7
            FRAME_THICKNESS = 3
            FONT_THICKNESS = 2
            MODEL = 'hog'  # default: 'hog', other one can be 'cnn' - CUDA accelerated (if available) deep-learning pretrained model

            #video = cv2.VideoCapture(f"C://Users//hai//Desktop//FACEREC//WIN_20220910_14_09_11_Pro_Trim.mp4")

            video = cv2.VideoCapture(request.form["img1"])

            
            


            known_faces = []
            recog=''


            for record in KNOWN_FACES_DIR:
                for person in record:
                    x=(person[-1]).split(".jpg")
                    x.remove('')
                    for name in x:
                        name+=".jpg"
                # Next we load every file of faces of known person
                #for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):

                        # Load an image
                        image = face_recognition.load_image_file(name)

                                # Get 128-dimension face encoding
                                # Always returns a list of found faces, for this purpose we take first face only (assuming one face per image as you can't be twice on one image)
                        encoding = face_recognition.face_encodings(image)[0]
                            

                                # Append encodings and name
                                
                            #encoding = pickle.load(open(f"C:/Users/hai/Desktop/PEOPLE/{name}/{filename}","rb"))
                        known_faces.append(encoding)
                        
    



    
            # Now let's loop over a folder of faces we want to label
                    while True:

                        # Load image
                        #print(f'Filename {filename}', end='')
                        
                        ret, image = video.read()
                        if not ret:
                            continue
                            
                        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        
                            # This time we first grab face locations - we'll need them to draw boxes
                        locations = face_recognition.face_locations(image ,model=MODEL)

                            # Now since we know loctions, we can pass them to face_encodings as second argument
                            # Without that it will search for faces once again slowing down whole process
                        encodings = face_recognition.face_encodings(image, locations)
                        c=True
                        """ can add model="large"(for slow nut accurate) or "small" """

                            # We passed our image through face_locations and face_encodings, so we can modify it
                            # First we need to convert it from RGB to BGR as we are going to work with cv2
                            #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                            # But this time we assume that there might be more faces in an image - we can find faces of dirrerent people
                        
                        for face_encoding in encodings:

                                # We use compare_faces (but might use face_distance as well)
                                # Returns array of True/False values in order of passed known_faces
                            results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
                            
                                # Since order is being preserved, we check if any face was found then grab index
                                # then label (name) of first matching known face withing a tolerance
                            
                            if np.count_nonzero(results)>3:# If at least one is true, get a name of first of found labels
                                    
                                        
                                recog=person[-1]
                                for i in range(len(arr)):
                                               
                                    if recog in arr[i]:
                                        cursor.execute("select * from arrested where images='%s'"%(recog,))
                                        d=cursor.fetchall()
                                        d=d[0]
                                        return render_template("results_arr.html",msg1=d[0],msg2=d[1],msg3=d[2],msg4=d[3],msg5=d[4],msg6=d[5])
                                for i in range(len(miss)):
                                               
                                    if recog in (miss[i] ):
                                        cursor.execute("select * from missing where images='%s'"%(recog,))
                                        d=cursor.fetchall()
                                        d=d[0]
                                        return render_template("results_miss.html",msg1=d[0],msg2=d[1],msg3=d[2],msg4=d[3],msg5=d[4],msg6=d[5],msg7=d[6])
                                for i in range(len(body)):
                                               
                                    if recog in (body[i]):
                                        cursor.execute("select * from body where images='%s'"%(recog,))
                                        d=cursor.fetchall()
                                        d=d[0]
                                        return render_template("results_body.html",msg1=d[0],msg2=d[1],msg3=d[2],msg4=d[3])
            return render_template("protosearch.html",msg="Record Not Found!!!")
                    
                                            
                            









@app.route('/prarrent',methods=['GET','POST'])
def prarrent():
    if request.method=='GET':
        return render_template('prarrent.html')

mycon2=sqltr.connect(host="localhost",user="root",passwd="root",database="record")

@app.route('/arr_add',methods=['GET','POST'])
def arr_add():
    if request.method == 'POST':
        
        img1=request.form["img1"]
        img2=request.form["img2"]
        img3=request.form["img3"]
        img4=request.form["img4"]
        img5=request.form["img5"]
        #file=os.path.abspath(file)
        files=img1+img2+img3+img4+img5
                
                    
        #file=os.path.abspath(os.path.join(file, os.pardir))
        #file = file.replace('\\','/')
        #file=file[::-1]
        #x=file.find('\\')
        #file=file[x+2:]
        
        
        name=request.form['name']
        address=request.form['address']
        dob=request.form['dob']
        rec=request.form['rec']
        rel=request.form['rel']
        med=request.form['med']
        cursor = mycon2.cursor()
        cursor.execute("INSERT INTO arrested(name,address,DOB,criminal_record,crime_relation,medical,images) VALUES('{}','{}','{}','{}','{}','{}','{}')".format(name,address,dob,rec,rel,med,files))
        mycon2.commit()
        return render_template('index.html')
    else:
        return render_template('prarrent.html')

    
@app.route('/prmisent',methods=['GET','POST'])
def prmisent():
    if request.method=='GET':
        return render_template('prmisent.html')


@app.route('/missing/',methods=['GET','POST'])
def missing():
    if request.method=="POST":
        cursor=mycon2.cursor()
        name=request.form['name']
        gender=request.form['gender']
        idm=request.form['idm']
        dob=request.form['dob']
        miss=request.form['miss']
        seen=request.form['seen']
        res=request.form['res']
        img1=request.form["img1"]
        img2=request.form["img2"]
        img3=request.form["img3"]
        img4=request.form["img4"]
        img5=request.form["img5"]
        #file=os.path.abspath(file)
        images=img1+img2+img3+img4+img5
        
        cursor.execute("INSERT INTO missing VALUES('{}','{}','{}','{}','{}','{}','{}','{}')".format(name,gender,idm,dob,miss,seen,res,images))
        mycon2.commit()
        return render_template('index.html')
    else:
        return render_template('prmisent.html')




    
@app.route('/prubent',methods=['GET','POST'])
def prubent():
    if request.method=='GET':
        return render_template('prubent.html')


@app.route('/body',methods=['GET','POST'])
def body():
    if request.method=="POST":
        cursor=mycon2.cursor()
        fdon=request.form['fdon']
        fdat=request.form['fdat']
        med=request.form['med']
        idm=request.form['id']
        img1=request.form["img1"]
        img2=request.form["img2"]
        img3=request.form["img3"]
        img4=request.form["img4"]
        img5=request.form["img5"]
        #file=os.path.abspath(file)
        images=img1+img2+img3+img4+img5
        
        cursor.execute("INSERT INTO body VALUES('{}','{}','{}','{}','{}')".format(fdon,fdat,med,idm,images))
        mycon2.commit()
        return render_template('index.html')
    else:
        return render_template('prubent.html')
    



    
@app.route('/prupdent',methods=['GET','POST'])
def prupdent():
    if request.method=='GET':
        return render_template('prupdent.html')
    
    
    



            
    




if __name__ == "__main__":
    app.run(debug=True)

