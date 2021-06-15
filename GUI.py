import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


from tkinter import messagebox


window = tk.Tk()
window.title("Project")
window.resizable(0,0)



load1 = Image.open("img/header.png")
photo1 = ImageTk.PhotoImage(load1)


header = tk.Button(window, image=photo1)
header.place(x=0, y=0)

canvas1 = Canvas(window, width = 1350, height=700, bg='ivory')
canvas1.place(x=5, y=165)

l1 = tk.Button(canvas1, text="Name", font=("Algerian",15))
l1.place(x=5, y=5)
t1 = tk.Entry(canvas1, width=50, bd=5)
t1.place(x=150, y=10)

l2 = tk.Button(canvas1, text="Age", font=("Algerian",15))
l2.place(x=5, y=50)
t2 = tk.Entry(canvas1, width=50, bd=5)
t2.place(x=150, y=55)

l3 = tk.Button(canvas1, text="Address", font=("Algerian",15))
l3.place(x=5, y=100)
t3 = tk.Entry(canvas1, width=50, bd=5)
t3.place(x=150, y=105)


b1= tk.Button(canvas1, text="Training", font=("Algerian",20), bg='orange', fg='red')
b1.place(x=10, y=180)

b2= tk.Button(canvas1, text="Generate dataset", font=("Algerian",20), bg='pink', fg='black')
b2.place(x=175, y=180)

load2= Image.open("img/canvas2.png")
photo2 = ImageTk.PhotoImage(load2)

canvas2 =  Canvas(window, width=500, height=250)
canvas2.place(x=5, y=400)
canvas2.create_image(250,125,image=photo2)

b3 = tk.Button(canvas2, text="Capture the image", font=("Algerian",20), bg="gray", fg="black")
b3.place(x=5, y=50)

b4 = tk.Button(canvas2, text="Predict face from live video", font=("Algerian", 20), bg="cyan", fg="black")
b4.place(x=5, y=150)

load3= Image.open('img/canvas3.png')
photo3 = ImageTk.PhotoImage(load3)

canvas3 = Canvas(window, width=280, height=530)
canvas3.place(x=550, y=170)
canvas3.create_image(140, 265, image=photo3)

window.geometry("1000x700")
window.mainloop()