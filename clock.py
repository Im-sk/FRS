from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from datetime import *
import time
from math import *


class Clock:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI Analog Clock")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#021e2f")
        #title = Label(self.root, text='Analog Clock', font=("times new roman", 50, "bold"), bg="#04444a",
        #              fg="white").place(x=0, y=50, relwidth=1)

        left_lbl = Label(self.root, bg="#08A3D2", bd=0)
        left_lbl.place(x=0, y=0, relheight=1, width=600)

        right_lbl = Label(self.root, bg="#031F3C", bd=0)
        right_lbl.place(x=600, y=0, relheight=1, relwidth=1)

        login_frame = Frame(self.root, bg="grey")
        login_frame.place(x=300, y=100, width=800, height=500)

        title = Label(login_frame, text="LOGIN HERE", width=26, font=("times new roman", 25, "bold"), bg="gray",
                      fg="black").place(x=200, y=30)
        f_name = Label(login_frame, text="User name", font=("times new roman", 18, "bold"), bg="gray", fg="black").place(x=250, y=120)
        self.txt_uname = Entry(login_frame, font=("times new roman", 18), bg="lightgray")
        self.txt_uname.place(x=250, y=160, width=250)

        password = Label(login_frame, text="Password", font=("times new roman", 18, "bold"), bg="gray", fg="black").place(x=250, y=210)
        self.txt_password = Entry(login_frame, font=("times new roman", 18), bg="lightgray")
        self.txt_password.place(x=250, y=240, width=250)

        btn_login = Button(login_frame, text="Log In",cursor="hand2",font=("times new roman", 18), bg="black",fg="white").place(x=250, y=310,width=150)

        btn_reg = Button(login_frame, text="Register account?",cursor="hand2",font=("times new roman", 15),bd=0, bg="gray",fg="brown").place(x=240, y=380,width=180)

        btn_forget = Button(login_frame, text="Forget Password?",cursor="hand2",font=("times new roman", 15),bd=0, bg="gray",fg="brown").place(x=20, y=410,width=180)


        self.lbl = Label(self.root, bg="#081923", bd=0)
        self.lbl.place(x=120, y=120, height=450, width=350)
        self.working()

    def clock_image(self, hr, min_, sec_):
        clock = Image.new("RGB", (400, 400), (8, 25, 35))
        draw = ImageDraw.Draw(clock)
        # Clock Image
        bg = Image.open("img/ck2.jpg")
        bg = bg.resize((400, 400), Image.ANTIALIAS)
        clock.paste(bg, (0, 0))
        # clock function
        origin = 200, 200
        # Clock Hour Lines
        draw.line((origin, 200 + 50 * sin(radians(hr)), 200 - 50 * cos(radians(hr))), fill="orange", width=3)
        clock.save("img/clock_new.png")

        # Clock Minutes Lines
        draw.line((origin, 200 + 80 * sin(radians(min_)), 200 - 80 * cos(radians(min_))), fill="yellow", width=3)
        clock.save("img/clock_new.png")

        # Clock Seconds Lines
        draw.line((origin, 200 + 100 * sin(radians(sec_)), 200 - 100 * cos(radians(sec_))), fill="green", width=4)
        draw.ellipse((195, 195, 210, 210), fill="black")
        clock.save("img/clock_new.png")

    def working(self):
        h = datetime.now().time().hour
        m = datetime.now().time().minute
        s = datetime.now().time().second
        hr = (h / 12) * 360
        min_ = (m / 60) * 360
        sec_ = (s / 60) * 360
        #         print(h,m,s)
        #         print(hr,min_,sec_)
        self.clock_image(hr, min_, sec_)
        self.img = ImageTk.PhotoImage(file="img/clock_new.png")
        self.lbl.config(image=self.img)
        self.lbl.after(200, self.working)


root = Tk()
obj = Clock(root)
root.mainloop()
