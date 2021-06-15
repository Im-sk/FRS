from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import pymysql


class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Form")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#081923")

        # background Image
        self.bg = ImageTk.PhotoImage(file="img/image4.jpg")
        bg = Label(self.root, image=self.bg).place(x=250, y=0, relwidth=1, relheight=1)

        # Left image
        self.left = ImageTk.PhotoImage(file="img/image2.jpg")
        left = Label(self.root, image=self.left, bg="white").place(x=120, y=100, width=400, height=500)

        frame1 = Frame(self.root, bg="white")
        frame1.place(x=480, y=100, width=750, height=500)
        title = Label(frame1, text="REGISTER HERE", font=("times new roman", 20, "bold"), bg="white", fg="green").place(
            x=50, y=30)

        # ----- first name

        f_name = Label(frame1, text="First name", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(
            x=50, y=100)
        self.txt_fname = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_fname.place(x=50, y=130, width=250)

        l_name = Label(frame1, text="Last name", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(
            x=370, y=100)
        self.txt_lname = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_lname.place(x=370, y=130, width=250)

        # --------------contact
        contact = Label(frame1, text="Contact No.", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(
            x=50, y=170)
        self.txt_contact = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_contact.place(x=50, y=200, width=250)

        email = Label(frame1, text="Email", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370,
                                                                                                               y=170)
        self.txt_email = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_email.place(x=370, y=200, width=250)

        # ---security ques
        question = Label(frame1, text="Security Question", font=("times new roman", 15, "bold"), bg="white",
                         fg="gray").place(x=50, y=240)
        self.cmb_quest = ttk.Combobox(frame1, font=("times new roman", 13), state='readonly', justify=CENTER)
        self.cmb_quest['values'] = (
        "Select", "What is your pet name", "What is your birth place", "Which is your favourite movie",
        "Which is your favourite sports")
        self.cmb_quest.place(x=50, y=270, width=250)
        self.cmb_quest.current(0)

        answer = Label(frame1, text="Answer", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370,
                                                                                                                 y=240)
        self.txt_answer = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_answer.place(x=370, y=270, width=250)

        # ---- password
        password = Label(frame1, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(
            x=50, y=310)
        self.txt_password = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_password.place(x=50, y=340, width=250)

        cpassword = Label(frame1, text="Confirm password", font=("times new roman", 15, "bold"), bg="white",
                          fg="gray").place(x=370, y=310)
        self.txt_cpassword = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_cpassword.place(x=370, y=340, width=250)

        # ---terms and condition---
        self.var_chk = IntVar()
        chk = Checkbutton(frame1, text="I Agree To Register", variable=self.var_chk, onvalue=1, offvalue=0, bg="white",
                          font=("times new roman", 11)).place(x=50, y=380)

        self.btn_img = ImageTk.PhotoImage(file="img/RegisterNow.jpg")
        btn_register = Button(frame1, image=self.btn_img, bd=0, cursor="hand2", command=self.register_data, width=300,
                              height=50).place(x=210, y=400)

        btn_login = Button(self.root, text="Sign In",command=self.redirect_log ,font=("times new roman", 15), bg="green", cursor="hand2").place(
            x=190, y=510, width=200)

    def redirect_log(self):
        self.root.destroy()
        import Login

    def clear(self):
        self.txt_fname.delete(0, END)
        self.txt_lname.delete(0, END)
        self.txt_contact.delete(0, END)
        self.txt_email.delete(0, END)
        self.txt_password.delete(0, END)
        self.txt_answer.delete(0, END)
        self.txt_cpassword.delete(0, END)
        self.cmb_quest.current(0)

    def register_data(self):
        if self.txt_fname.get() == "" or self.txt_lname.get() == "" or self.txt_email.get() == "" or self.txt_contact.get() == "" or self.cmb_quest.get() == "select" or self.txt_answer.get() == "" or self.txt_password.get() == "" or self.txt_cpassword.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        elif self.txt_password.get() != self.txt_cpassword.get():
            messagebox.showerror("Error", "Password and Confirm password should be same", parent=self.root)
        elif self.var_chk.get() == 0:
            messagebox.showerror("Error", "Please Agree our terms and Condition", parent=self.root)
        else:  # -----------if everything Ok then set connection and fetch or add information
            try:
                con = pymysql.connect(host="localhost", user="root", password="", database="employee")
                cur = con.cursor()
                cur.execute("select * from emp where email=%s",
                            self.txt_email.get())  # ---- check if same email, then enter again
                row = cur.fetchone()
                print(row)
                if row != None:
                    messagebox.showerror("Error", "user already exists please try with another email", parent=self.root)
                else:  # ------ if user is new then add
                    cur.execute(
                        "insert into emp(f_name,l_name,contact,email,question,answer,password) values(%s,%s,%s,%s,%s,%s,%s)",
                        (self.txt_fname.get(),
                         self.txt_lname.get(),
                         self.txt_contact.get(),
                         self.txt_email.get(),
                         self.cmb_quest.get(),
                         self.txt_answer.get(),
                         self.txt_password.get()

                         ))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", " Registration success", parent=self.root)
                    self.clear()

            except Exception as es:  # ----- message for other errors or exceptions
                messagebox.showerror("Error", f"error due to:{str(es)}", parent=self.root)


root = Tk()
obj = Register(root)
root.mainloop()