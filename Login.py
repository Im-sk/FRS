from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk, messagebox
import pymysql
from datetime import *
import time
from math import *



class log:
    def __init__(self, root):
        self.root=root
        self.root.title("LOGIN")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="black")

        self.bg = ImageTk.PhotoImage(file="img/image5.jpg")
        bg = Label(self.root, image=self.bg).place(x=250, y=0, relwidth=1, relheight=1)
        #
        # self.left = ImageTk.PhotoImage(file="img/A-Criminals-always-returns-to-the-scene-of-the-crime.jpg")
        # left = Label(self.root, image=self.left, bg="white").place(x=80, y=100, width=400, height=500)
        left_lbl = Label(self.root, bg="#081923", bd=0)
        left_lbl.place(x=0, y=0, relheight=1, width=500)

        # right_lbl = Label(self.root, bg="#031F3C", bd=0)
        # right_lbl.place(x=600, y=0, relheight=1, relwidth=1)

        frame1 = Frame(self.root, bg="grey")
        frame1.place(x=300, y=100, width=800, height=500)

        title=Label(frame1,text="LOGIN HERE",width=26,font=("times new roman",25,"bold"),bg="gray",fg="black").place(x=200,y=30)

        f_name = Label(frame1, text="E-mail", font=("times new roman", 18, "bold"), bg="gray", fg="black").place(x=250, y=120)
        self.txt_uname = Entry(frame1, font=("times new roman", 18), bg="lightgray")
        self.txt_uname.place(x=250, y=155, width=250)

        password = Label(frame1, text="Password", font=("times new roman", 18, "bold"), bg="gray", fg="black").place(x=250, y=210)
        self.txt_password = Entry(frame1, font=("times new roman", 18), bg="lightgray")
        self.txt_password.place(x=250, y=240, width=250)

        btn_login = Button(frame1, text="Log In",command=self.login,cursor="hand2",font=("times new roman", 18), bg="black",fg="white").place(x=250, y=310,width=150)

        btn_reg = Button(frame1, text="Register account?",cursor="hand2",command=self.redirect,font=("times new roman", 15),bd=0, bg="gray",fg="brown").place(x=250, y=380,width=180)

        btn_forget = Button(frame1, text="Forget Password?",cursor="hand2",command=self.forget_password,font=("times new roman", 15),bd=0, bg="gray",fg="brown").place(x=250, y=410,width=180)

        self.lbl = Label(self.root, bg="#081923", bd=0)
        self.lbl.place(x=120, y=120, height=450, width=350)
        self.working()

        #--------------------- Layout over ------------------------------------------------------
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

    # ------------- a function to reset data after process ends -----------
    def reset(self):
        self.cmb_quest.current(0)
        self.txt_newpass.delete(0,END)
        self.txt_answer.delete(0,END)
        self.txt_password.delete(0,END)
        self.txt_uname.delete(0,END)



    def forget_pass(self):    #----- for forget password-----
        if self.cmb_quest.get()=="select" or self.txt_answer.get()=="" or self.txt_newpass.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.root2)     #----- if required fields are not filled -----
        else:            #----- if ok then form the connection -----
            try:
                con = pymysql.connect(host="localhost", user="root", password="", database="employee")
                cur = con.cursor()
                cur.execute("select * from emp where email=%s and question=%s and answer=%s" , (self.txt_uname.get(),self.cmb_quest.get(),self.txt_answer.get()))
                row = cur.fetchone()
                if row == None:            #----- if data entered for password reset not found then --------------
                    messagebox.showerror("Error", "Please enter valid credentials", parent=self.root2)
                else:               #------- if found then reset and update---------
                    cur.execute("update emp set password=%s where email=%s",(self.txt_newpass.get(),self.txt_uname.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo("success","password has been reseted",parent=self.root2)
                    self.reset()
                    self.root2.destroy()                #--------- after resetting destroy all windows except loging page ---------
            except Exception as es:
                messagebox.showerror("Error",f"due to:{str(es)}",parent=self.root)


    def forget_password(self):
        if self.txt_uname.get()=="":           #------ don't allow to reset password unless username entered -----------
            messagebox.showerror("Error","please enter username to reset password",parent=self.root)
        else:               #--------- if entered then allow to reset password and set connection -----------
            try:
                con=pymysql.connect(host="localhost",user="root",password="",database="employee")
                cur=con.cursor()
                cur.execute("select * from emp where email=%s",(self.txt_uname.get()))
                row=cur.fetchone()
                if row==None:            #------------ if not a valid username -------------
                    messagebox.showerror("Error","Please enter valid username to reset password",parent=self.root)
                else:                  #------ if valid, then open another window -----------
                    con.close()
                    self.root2 = Toplevel()         #-------- will open on login window----------
                    self.root2.title("Forget Password")
                    self.root2.geometry("350x400+495+150")
                    self.root2.configure(bg="white")
                    self.root2.focus_force()
                    self.root2.grab_set()

                    t = Label(self.root2, text="forget password", font=("times new roman", 20, "bold"), bg="white",fg="red").place(x=0, y=10, relwidth=1)

                    question = Label(self.root2, text="Security Question", font=("times new roman", 15, "bold"),bg="white", fg="gray").place(x=50, y=100)
                    self.cmb_quest = ttk.Combobox(self.root2, font=("times new roman", 13), state='readonly',justify=CENTER)
                    self.cmb_quest['values'] = ("Select", "What is your pet name", "What is your birth place", "Which is your favourite movie","Which is your favourite sports")
                    self.cmb_quest.place(x=50, y=130, width=250)
                    self.cmb_quest.current(0)

                    answer = Label(self.root2, text="Answer", font=("times new roman", 15, "bold"), bg="white",fg="gray").place(x=50, y=180)
                    self.txt_answer = Entry(self.root2, font=("times new roman", 15), bg="lightgray")
                    self.txt_answer.place(x=50, y=210, width=250)

                    newpass = Label(self.root2, text="New password", font=("times new roman", 15, "bold"), bg="white",fg="gray").place(x=50, y=260)
                    self.txt_newpass = Entry(self.root2, font=("times new roman", 15), bg="lightgray")
                    self.txt_newpass.place(x=50, y=290, width=250)

                    btn_change_password = Button(self.root2, text="Reset password",command=self.forget_pass,bg="green", fg="white",font=("times new roman", 15, "bold")).place(x=80, y=340)

            except Exception as es:
                messagebox.showerror("Error",f"due to:{str(es)}",parent=self.root)

        #------------------------ layout of password resert window over ---------------------------------------------

    def redirect(self):
        self.root.destroy()                #--------- if not registered then redirect to the register page ----------------
        import register

    def login(self):            #------------------- for proper login --------------------
        if self.txt_uname.get()=="" or self.txt_password.get()=="":
            messagebox.showerror("Error","Enter details",parent=self.root)
        else:
            try:
                con=pymysql.connect(host="localhost",user="root",password="",database="employee")
                cur=con.cursor()
                cur.execute("select * from emp where email=%s and password=%s",(self.txt_uname.get(),self.txt_password.get()))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","invalid credentials",parent=self.root)
                else:
                    messagebox.showinfo("Success","Welcome",parent=self.root)
                    self.root.destroy()
                    import Main2
                con.close()
            except Exception as es:
                messagebox.showerror("Error",f"due to:{str(es)}",parent=self.root)

root = Tk()
obj =log(root)
root.mainloop()