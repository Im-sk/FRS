import tkinter as tk
from tkinter import *
import cv2
import os
from PIL import Image, ImageTk
import numpy as np
import mysql.connector
from tkinter import messagebox

window = tk.Tk()
window.configure(bg="black")
window.title("BE Project")
window.resizable(0, 0)

load1 = Image.open("img/header.png")
photo1 = ImageTk.PhotoImage(load1)

header = tk.Button(window, image=photo1)
header.place(x=5, y=0)

canvas1 = Canvas(window, width=1150, height=650, bg='ivory')
canvas1.place(x=5, y=120)

l1 = tk.Button(canvas1, text="Name", font=("Algerian", 15))
l1.place(x=10, y=15)
t1 = tk.Entry(canvas1, width=50, bd=7)
t1.place(x=150, y=15)

l2 = tk.Button(canvas1, text="Age", font=("Algerian", 15))
l2.place(x=10, y=65)
t2 = tk.Entry(canvas1, width=50, bd=7)
t2.place(x=150, y=65)

l3 = tk.Button(canvas1, text="Place", font=("Algerian", 15))
l3.place(x=10, y=115)
t3 = tk.Entry(canvas1, width=50, bd=7)
t3.place(x=150, y=115)

l4 = tk.Button(canvas1, text="Crime", font=("Algerian", 15))
l4.place(x=10, y=165)
t4 = tk.Entry(canvas1, width=50, bd=7)
t4.place(x=150, y=165)


def generate_dataset():
    if (t1.get() == "" or t2.get() == "" or t3.get() == "" or t4.get() == ""):
        messagebox.showinfo("Result", "Please provide complete details of the user...")
    else:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="Authorized_user"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * from my_table")
        myresult = mycursor.fetchall()

        id = 1
        for x in myresult:
            id += 1

        sql = "insert into my_table(id,name,age,address,crime) values(%s, %s, %s, %s, %s)"
        val = (id, t1.get(), t2.get(), t3.get(), t4.get())
        mycursor.execute(sql, val)
        mydb.commit()

        face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        def face_cropped(img):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            # scaling factor = 1.3
            # minimum neighbor = 5

            if faces is ():
                return None
            for (x, y, w, h) in faces:
                cropped_face = img[y:y + h, x:x + w]
            return cropped_face

        cap = cv2.VideoCapture(0)
        img_id = 0

        while True:
            ret, frame = cap.read()
            if face_cropped(frame) is not None:
                img_id += 1
                face = cv2.resize(face_cropped(frame), (200, 200))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                file_name_path = "data/user." + str(id) + "." + str(img_id) + ".jpg"
                cv2.imwrite(file_name_path, face)
                cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

                cv2.imshow("Cropped face", face)

            if cv2.waitKey(1) == 13 or int(img_id) == 200:  # 13 is the ASCII character of Enter
                break

        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Result", "Generating dataset is completed.....")


b1 = tk.Button(canvas1, text="Register Person", font=("Algerian", 20), bg='#2F4F4F', fg='black',command=generate_dataset)
b1.place(x=10, y=220)


def train_classifier():
    data_dir = "E:/xProjects/FRS/data"
    path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]

    faces = []
    ids = []

    for image in path:
        img = Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(os.path.split(image)[1].split(".")[1])

        faces.append(imageNp)
        ids.append(id)

    ids = np.array(ids)

    # Train and save classifier
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write("classifier.xml")
    messagebox.showinfo("Result", "Model trained completed.....")


b2 = tk.Button(canvas1, text="Train Classifier", font=("Algerian", 20), bg='#2F4F4F', fg='red', command=train_classifier)
b2.place(x=10, y=300)

load2 = Image.open("img/canvas2.png")
photo2 = ImageTk.PhotoImage(load2)

canvas2 = Canvas(window, width=500, height=250)
canvas2.place(x=10, y=490)


# canvas2.create_image(250,125,image=photo2)

def capture_image():
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
    else:
        ret = False

    face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    # scaling factor = 1.3
    # minimum neighbor = 5

    if faces is ():
        print("No face detected..")
        return None
    else:
        for (x, y, w, h) in faces:
            cropped_face = frame[y:y + h, x:x + w]
        cv2.imwrite("img/captured_image.jpg", cropped_face)

        load = Image.open("img/captured_image.jpg")
        photo = ImageTk.PhotoImage(load)

        # Labels can be text or images
        img = Label(canvas3, image=photo, width=200, height=200)
        img.image = photo

        img.place(x=0, y=5)

        cap.release()

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    for (x, y, w, h) in faces:
        id, pred = clf.predict(gray[y:y + h, x:x + w])
        # confidence = int(100*(1-pred/300))

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="Authorized_user"
        )
        mycursor = mydb.cursor()

        mycursor.execute("select name,age,address,crime from my_table where id=" + str(id))
        s = mycursor.fetchall()

        a1 = tk.Label(canvas3, text="Name = ", font=("Algerian", 20))
        a1.place(x=5, y=250)

        b1 = tk.Label(canvas3, text=s[0][0], font=("Algerian", 20))
        b1.place(x=150, y=250)

        c1 = tk.Label(canvas3, text="Age = ", font=("Algerian", 20))
        c1.place(x=5, y=300)

        d1 = tk.Label(canvas3, text=s[0][1], font=("Algerian", 20))
        d1.place(x=150, y=300)

        e1 = tk.Label(canvas3, text="Place = ", font=("Algerian", 20))
        e1.place(x=5, y=350)

        f1 = tk.Label(canvas3, text=s[0][2], font=("Algerian", 20))
        f1.place(x=150, y=350)

        g1 = tk.Label(canvas3, text="Crime = ", font=("Algerian", 20))
        g1.place(x=5, y=400)

        h1 = tk.Label(canvas3, text=s[0][3], font=("Algerian", 20))
        h1.place(x=150, y=400)


b3 = tk.Button(canvas2, text="Capture  Image", font=("Algerian", 20), bg="#2F4F4F", fg="black",
               command=capture_image)
b3.place(x=5, y=10)


###
################################################
def detect_face():
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

        coords = []

        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            id, pred = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int(100 * (1 - pred / 300))

            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="Authorized_user"
            )
            mycursor = mydb.cursor()
            mycursor.execute("select name from my_table where id=" + str(id))
            s = mycursor.fetchone()
            s = '' + ''.join(s)

            if confidence > 74:
                cv2.putText(img, s, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
            else:
                cv2.putText(img, "UNKNOWN", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

            coords = [x, y, w, h]
        return coords

    def recognize(img, clf, faceCascade):
        coords = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "Face", clf)
        return img

    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, img = video_capture.read()
        img = recognize(img, clf, faceCascade)
        cv2.imshow("face detection", img)

        if cv2.waitKey(1) == 13:
            break

    video_capture.release()
    cv2.destroyAllWindows()


b4 = tk.Button(canvas2, text="Video Surveillance", font=("Algerian", 20), bg="#2F4F4F", fg="black", command=detect_face)
b4.place(x=5, y=100)

load3 = Image.open('img/canvas3.png')
photo3 = ImageTk.PhotoImage(load3)

load3 = Image.open('img/canvas3.png')
photo3 = ImageTk.PhotoImage(load3)

canvas3 = Canvas(window, width=480, height=530)
canvas3.place(x=555, y=150)
# canvas3.create_image(140, 265, image=photo3)

window.geometry("1065x1000")
window.mainloop()