#from fileinput import filename
from tkinter import *
from tkinter import messagebox

from Studentpage import  StudentClass
from PIL import Image, ImageTk
from notifier import *

from changepasswordpage import ChangePasswordClass
from coursepage import CourseClass
from departmentpage import DepartmentClass
from reportpage1 import Report1Class
from reportpage2 import Report2Class
from reportpage3 import Report3Class
from userpage import UserClass



class homepage:

    def __init__(self):
        self.ut = None
        self.window = Tk()

         #-------------- Screen Setting------------------

        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()

        w1 = int(w/2)
        h1 = int(h/2)
        x1 = int(w/4)
        y1 = int(h/4)

        self.window.minsize(w1, h1)
        self.window.title("Home-Page")
        self.window.geometry("%dx%d+%d+%d"% (w1, h1, x1, y1))
        self.window.state("zoomed")


       #---------------- Frames -----------------------------

        f1_width = 200
        f2_width = w-f1_width
        self.f1 = Frame(self.window,background='light grey')
        self.f2 = Frame(self.window, background='#E3E1D9')
        self.f1.place(x=0, y=0, width=f1_width, height=h)
        self.f2.place(x=f1_width, y=0, width=f2_width, height=h)

      #------------- Menu --------------------

        x1 = 5
        y1 = 10
        b1_width = f1_width-10
        b1_height = 40
        y_diff = b1_height+2
        if self.ut == 'Admin':
            mycolor1='#3D52A0'
        else:
            mycolor1='#6e43b0'
        mycolor2= '#8697C4'
        myfont1 = ('Segoe UI',12,'bold')


        self.b1 = Button(self.window, text = 'Student', borderwidth  = '1', font = myfont1, relief="solid",
                         command = lambda: StudentClass(self.window))
        self.b2 = Button(self.window, text='Department', borderwidth='1', font=myfont1, relief="solid",
                         command =  lambda: DepartmentClass(self.window))
        self.b3 = Button(self.window, text='Course', borderwidth  = '1', font=myfont1,relief="solid",
                         command=lambda: CourseClass(self.window))  # to open dependent window
        self.b4 = Button(self.window, text='User',font=myfont1,borderwidth = '1',relief="solid",
                         command=lambda: UserClass(self.window))  # to open dependent window
        self.b5 = Button(self.window, text='Report', font=myfont1,borderwidth  = '1',relief="solid",
                         command=lambda: Report1Class(self.window))  # to open dependent window
        self.b6 = Button(self.window, text='Report By Department',borderwidth  = '1',relief="solid",
                         font=myfont1, command=lambda:Report2Class(self.window))  # to open dependent window
        self.b7 = Button(self.window, text='Report By DOB', font=myfont1,borderwidth  = '1',relief="solid",
                         command=lambda: Report3Class(self.window))  # to open dependent window
        self.b8 = Button(self.window,text='Change Password',font=myfont1,borderwidth  = '1',relief="solid",
                         command=lambda: ChangePasswordClass(self.window,'uname'))  # to open dependent window
        self.b9 = Button(self.window,text='Logout', font=myfont1,borderwidth='1', relief="solid",
                         command=self.quitter)

        if self.ut == "Employee":
            self.b6['state'] = 'disable'

        #------------- Placement ----------------

        self.b1.place(x=x1,  y=y1, width=b1_width, height=b1_height)
        y1+=y_diff

        self.b2.place(x=x1, y=y1+2, width=b1_width, height=b1_height)
        y1 += y_diff

        self.b3.place(x=x1, y=y1+5, width=b1_width, height=b1_height)
        y1 += y_diff
        #if self.ut == 'Admin':

        self.b4.place(x=x1, y=y1+9, width=b1_width, height=b1_height)
        y1 += y_diff

        self.b5.place(x=x1, y=y1+10, width=b1_width, height=b1_height)
        y1 += y_diff

        self.b6.place(x=x1, y=y1+14, width=b1_width, height=b1_height)
        y1 += y_diff
        #if self.ut == 'Admin':

        self.b7.place(x=x1, y=y1+15, width=b1_width, height=b1_height)
        y1 += y_diff

        self.b8.place(x=x1, y=y1+17, width=b1_width, height=b1_height)
        y1 += y_diff

        self.b9.place(x=x1, y=y1+19, width=b1_width, height=b1_height)
        y1 += y_diff

        #------------------ Background In Frame-2 -----------------------

        self.bkimg1 = Image.open("student_images//university_image.jpg").resize((f2_width, h))
        self.bkping1 = ImageTk.PhotoImage(self.bkimg1)
        self.bklbl = Label(self.f2,image=self.bkping1)
        self.bklbl.place(x=0, y=0)

        self.window.mainloop()


    def quitter(self):
        ans = messagebox.askquestion("Confirmation","Are you sure to Logout??",parent=self.window)
        if ans=='yes':
            self.window.destroy()
            from loginpage import LoginClass
            LoginClass()


if __name__ == '__main__':
    homepage()

