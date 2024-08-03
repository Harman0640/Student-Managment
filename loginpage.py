from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Treeview
import pymysql
from tkcalendar import DateEntry
from PIL import Image,ImageTk

class LoginClass:
    def __init__(self):
        self.window = Tk()
        self.window.title("Royal Hotel\Login")


        # ------------- settings ------------------
        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()

        w1 = int(w/2)
        h1 = int(h/2)
        x1 = int(w/4)
        y1 = int(h/4)
        self.window.minsize(w1,h1)
        self.window.geometry("%dx%d+%d+%d"%(w1,h1,x1,y1))#wxh+x+y
        # ------------- widgets ----------------------------------
        mycolor1 = '#EDE8F5'
        mycolor2 = '#7091E6'
        myfont1 = ('Cambria',13,'bold')
        self.window.config(background=mycolor1)

        self.hdlbl = Label(self.window,text='User',background="grey",fg="black",font=('Cambria',20,'bold'))


        self.L1 = Label(self.window,text='Username',fg="black",font=myfont1)
        self.L2 = Label(self.window,text='Password',fg="black",font=myfont1)
        self.L3 = Label(self.window,text='Usertype',fg="black",font=myfont1)
        self.L4 = Label(self.window,text='Pic',background="grey",fg="black",font=myfont1)

        self.t1 = Entry(self.window,font=myfont1)
        self.t2 = Entry(self.window,font=myfont1,show='*')



        #----------------- buttons ---------------------
        self.b1 = Button(self.window,text='Login',font=myfont1,background="grey",command=self.checkData)


        # ------------placement -----------------
        self.hdlbl.place(x=0,y=0,width=w1,height=70)
        x1 = 100
        y1 =100
        x_diff = 150
        y_diff = 50

        self.L1.place(x=x1,y=y1)
        self.t1.place(x=x1+x_diff,y=y1)
        y1+=y_diff
        self.L2.place(x=x1,y=y1)
        self.t2.place(x=x1+x_diff,y=y1)
        y1+=y_diff
        self.b1.place(x=x1+150,y=y1,width=150,height=40)



        #------call required functions ----------
        self.databaseConnection()
        self.clearPage()

        self.window.mainloop()


    def databaseConnection(self):

        try:
            self.conn = pymysql.connect(host='localhost',db='mycollegemanger_db',user='root',password='')
            self.curr = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Connection Error","Error in Database Connection : \n"+str(e),parent=self.window)


    def checkData(self):
        try:
            qry = 'select * from usertable  where username=%s and password=%s'
            rowcount = self.curr.execute(qry ,(self.t1.get(),self.t2.get()) )
            rowdata = self.curr.fetchone()
            if rowdata:
                uname = rowdata[0]
                utype = rowdata[2]
                messagebox.showinfo("Success",f"Welcome {uname} [{utype}]",parent=self.window)
                self.window.destroy()
                from Homepage import homepage
                homepage()
            else:
                messagebox.showwarning("Failure","Wrong username or password",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in fetching : \n"+str(e),parent=self.window)

    def clearPage(self):
        self.t1.delete(0,END)
        self.t2.delete(0,END)

#--------- for testing only ------------
if __name__ == '__main__':
    LoginClass()