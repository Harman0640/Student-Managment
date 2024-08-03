from tkinter import *
from tkinter import messagebox
#from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Treeview

#import face_recognition
import pymysql
# from tkcalendar import DateEntry
# from PIL import Image,ImageTk

class UserClass:
    defaultname="default_image.png"
    def __init__(self,hwindow):
        self.window = Toplevel(hwindow)
        self.window.title("Admin / User")

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

        self.hdlbl = Label(self.window,text='User',background='grey',fg='black',font=('Cambria',20,'bold'))


        self.L1 = Label(self.window,text='Username',background=mycolor1,font=myfont1,borderwidth=3)
        self.L2 = Label(self.window,text='Password',background=mycolor1,font=myfont1,borderwidth=3)
        self.L3 = Label(self.window,text='Usertype',background=mycolor1,font=myfont1,borderwidth=3)
        # self.L4 = Label(self.window,text='Pic',background=mycolor1,font=myfont1)

        self.t1 = Entry(self.window,font=myfont1,borderwidth=3)
        self.t2 = Entry(self.window,font=myfont1,show='*',borderwidth=3)
        self.v1 = StringVar()
        self.v2 = StringVar()
        self.c1 = Combobox(self.window,values=['Admin','Employee'],
                           textvariable=self.v1,font=myfont1,state='readonly')


        # ------------------ table ---------------------
        self.mytable1 = Treeview(self.window, columns=['c1', 'c2'], height=10)

        self.mytable1.heading('c1', text='Username')
        self.mytable1.heading('c2', text='Usertype')
        self.mytable1['show'] = 'headings'

        self.mytable1.column('c1', width=300, anchor='center')
        self.mytable1.column('c2', width=300, anchor='center')
        self.mytable1.bind("<ButtonRelease-1>",lambda e: self.getSelectedRow())

        #----------------- buttons ---------------------
        self.b1 = Button(self.window,text='Save',font=myfont1,background='grey',fg='black',command=self.saveData,borderwidth=3)
        self.b2 = Button(self.window,text='Update',font=myfont1,background='grey',fg='white',command=self.updateData,borderwidth=3)
        self.b3 = Button(self.window,text='Delete',font=myfont1,background='grey',fg='white',command=self.deleteData,borderwidth=3)
        self.b4 = Button(self.window,text='Fetch',font=myfont1,background='grey',fg='black',command=self.fetchData,borderwidth=3)
        self.b5 = Button(self.window,text='Search',font=myfont1,background='grey',fg='black',command=self.showAllData,borderwidth=3)
        self.b7 = Button(self.window,text='Reset',font=myfont1,background='grey',fg='black',command=self.clearPage,borderwidth=3)


        # ------------placement -----------------
        self.hdlbl.place(x=0,y=0,width=w,height=70)
        x1 = 10
        y1 =100
        x_diff = 150
        y_diff = 50

        self.L1.place(x=x1,y=y1)
        self.t1.place(x=x1+x_diff,y=y1)
        self.b4.place(x=x1+x_diff*2+80,y=y1,width=100,height=25)
        self.mytable1.place(x=x1+x_diff*3+70,y=y1)
        y1+=y_diff
        self.L2.place(x=x1,y=y1)
        self.t2.place(x=x1+x_diff,y=y1)
        y1+=y_diff
        self.L3.place(x=x1,y=y1)
        self.c1.place(x=x1+x_diff,y=y1)
        self.b5.place(x=x1+x_diff*2+80,y=y1,width=100,height=25)
        y1+=y_diff

        y1+=y_diff
        self.b1.place(x=x1,y=y1,width=150,height=40)
        self.b2.place(x=x1+x_diff,y=y1,width=150,height=40)
        self.b3.place(x=x1+x_diff*2,y=y1,width=150,height=40)
        y1+=y_diff
        self.b7.place(x=x1,y=y1,width=150,height=40)



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

    def saveData(self):
        if self.validationCheck()==False:
            return # end this function now
        try:
            #	username	password	usertype	pic

            qry = 'insert into usertable values(%s,%s,%s)'
            rowcount = self.curr.execute(qry ,(self.t1.get(), self.t2.get(), self.v1.get()) )
            self.conn.commit()
            if rowcount==1:


                messagebox.showinfo("Success","User Record Saved successfully",parent=self.window)
                self.clearPage()
            else:
                messagebox.showwarning("Failure","User Record not Saved y",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in insertion : \n"+str(e),parent=self.window)

    def updateData(self):
        if self.validationCheck()==False:
            return # end this function now
        try:
            qry = 'update usertable set password=%s, usertype=%s,  where username=%s'
            rowcount = self.curr.execute(qry ,( self.t2.get(), self.v1.get(), self.t1.get()) )
            self.conn.commit()
            if rowcount==1:


                messagebox.showinfo("Success","User Record Updated successfully",parent=self.window)
                self.clearPage()
            else:
                messagebox.showwarning("Failure","User Record not Updated ",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in insertion : \n"+str(e),parent=self.window)

    def deleteData(self):
        ans = messagebox.askquestion("Confirmation","Are you sure to delete??",parent=self.window)
        if ans=='yes':
            try:
                qry = 'delete from usertable where username=%s'
                rowcount = self.curr.execute(qry ,(self.t1.get()) )
                self.conn.commit()
                if rowcount==1:

                    #-----------------------------------------------------------
                    messagebox.showinfo("Success","User Record Deleted successfully",parent=self.window)
                    self.clearPage()
                else:
                    messagebox.showwarning("Failure","User Record not Deleted ",parent=self.window)
            except Exception as e:
                messagebox.showerror("Query Error","Error in insertion : \n"+str(e),parent=self.window)

    def getSelectedRow(self):
        id = self.mytable1.focus()
        row_record = self.mytable1.item(id)
        row = row_record['values']
        col0 = row[0]
        self.fetchData(col0)

    def fetchData(self,pcolumn=None):
        if pcolumn==None:
            un  = self.t1.get()
        else:
            un = pcolumn
        try:
            qry = 'select * from usertable  where username=%s'
            rowcount = self.curr.execute(qry ,(un) )
            rowdata = self.curr.fetchone()
            self.clearPage()
            if rowdata:
                # set data in fields
                self.t1.insert(0,rowdata[0])
                self.t2.insert(0,rowdata[1])
                self.v1.set(rowdata[2])

                self.b1['state']='disable'
                self.b2['state']='normal'
                self.b3['state']='normal'
            else:
                messagebox.showwarning("Empty","No Record Found",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in fetching : \n"+str(e),parent=self.window)

    def clearPage(self):
        self.t1.delete(0,END)
        self.t2.delete(0,END)
        self.c1.set("Choose Usertype")
        self.showAllData()

        self.b1['state']='normal'
        self.b2['state']='disable'
        self.b3['state']='disable'


    def showAllData(self):
        try:
            self.mytable1.delete(*self.mytable1.get_children())
            utype = self.v1.get()
            if utype=="Choose Usertype":
                utype=""
            qry = 'select * from usertable where usertype like %s'
            rowcount = self.curr.execute(qry,(utype+"%") )
            rowdata = self.curr.fetchall()
            if rowdata:
                for row in rowdata:
                    r1 = [row[0],row[2]]
                    self.mytable1.insert('',END,values=r1)
            else:
                messagebox.showwarning("Empty","No Record Found",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in fetching : \n"+str(e),parent=self.window)

    def validationCheck(self):
        return True



#--------- for testing only ------------
if __name__ == '__main__':
    dummy_home=Tk()
    UserClass(dummy_home)
    dummy_home.mainloop()