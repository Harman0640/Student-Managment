# import Numpy as np
from tkinter import *
from tkinter import messagebox
#from tkinter.filedialog import askopenfilename
#from tkinter.ttk import Combobox, Treeview
import pymysql
#from tkcalendar import DateEntry
#from PIL import Image,ImageTk

class ChangePasswordClass:
    def __init__(self,hwindow,uname):
        self.uname = uname
        self.window = Toplevel(hwindow)
        self.window.title("My College Manager\Change Password")

        # ------------- settings ------------------
        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()

        x1 = 200
        w1 = w-x1
        y1 = 50
        h1 = h-y1-100
        self.window.minsize(w1,h1)
        self.window.geometry("%dx%d+%d+%d"%(w1,h1,x1,y1))#wxh+x+y

        # ------------- widgets ----------------------------------
        mycolor1 = '#EDE8F5'
        mycolor2 = '#7091E6'
        myfont1 = ('Cambria',13,'bold')
        self.window.config(background=mycolor1)

        self.hdlbl = Label(self.window,text='Change Password',background='grey',font=('Cambria',20,'bold'))


        self.L1 = Label(self.window,text='Current Password',background=mycolor1,font=myfont1)
        self.L2 = Label(self.window,text='New Password',background=mycolor1,font=myfont1)
        self.L3 = Label(self.window,text='Confirm Password',background=mycolor1,font=myfont1)

        self.t1 = Entry(self.window,font=myfont1,show='*',borderwidth=3)
        self.t2 = Entry(self.window,font=myfont1,show='*',borderwidth=3)
        self.t3 = Entry(self.window,font=myfont1,show='*',borderwidth=3)

        #----------------- buttons ---------------------
        self.b1 = Button(self.window,text='Change',font=myfont1,background='grey',command=self.updateData,borderwidth=3)

        # ------------placement -----------------
        self.hdlbl.place(x=0,y=0,width=w,height=70)
        x1 = 10
        y1 =100
        x_diff = 150
        y_diff = 50

        self.L1.place(x=x1,y=y1)
        self.t1.place(x=x1+x_diff+20,y=y1)
        y1+=y_diff
        self.L2.place(x=x1,y=y1)
        self.t2.place(x=x1+x_diff+20,y=y1)
        y1+=y_diff
        self.L3.place(x=x1,y=y1)
        self.t3.place(x=x1+x_diff+20,y=y1)
        y1+=y_diff

        y1+=y_diff
        self.b1.place(x=x1,y=y1,width=150,height=40)


        #------call required functions ----------
        self.databaseConnection()

        self.window.mainloop()



    def databaseConnection(self):

        try:
            self.conn = pymysql.connect(host='localhost',db='mycollegemanger_db',user='root',password='')
            self.curr = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Connection Error","Error in Database Connection : \n"+str(e),parent=self.window)


    def updateData(self):
        if self.t2.get()!=self.t3.get():
                messagebox.showwarning("Failure","Confirm Password Carefully",parent=self.window)
                return
        try:
            qry = 'update usertable set password=%s where username=%s and password=%s'
            rowcount = self.curr.execute(qry ,( self.t2.get(),  self.uname,     self.t1.get()) )
            self.conn.commit()
            if rowcount == 1:

                messagebox.showinfo("Success","Password Changed successfully",parent=self.window)
                self.clearPage()
            else:
                messagebox.showwarning("Failure","Wrong Current Password ", parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in insertion : \n"+str(e), parent=self.window)


    def clearPage(self):
        self.t1.delete(0,END)
        self.t2.delete(0,END)
        self.t3.delete(0,END)


if __name__ == '__main__':
    dummy_home=Tk()
    ChangePasswordClass(dummy_home,'uname')
    dummy_home.mainloop()


