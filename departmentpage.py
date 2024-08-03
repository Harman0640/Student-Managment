from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Treeview
import pymysql
from tkcalendar import DateEntry
from PIL import Image,ImageTk

class DepartmentClass:
    def __init__(self,hwindow):
        self.window = Toplevel(hwindow)
        self.window.title("My College Manager\Department")

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
        mycolor1 = '#E3E1D9'
        mycolor2 = '#E3E1D9'
        myfont1 = ('Cambria',13,'bold')
        self.window.config(background=mycolor1)

        self.hdlbl = Label(self.window,text='Department',background="grey",font=('Cambria',20,'bold'))


        self.L1 = Label(self.window,text='Department Name',background=mycolor1,font=myfont1)
        self.L2 = Label(self.window,text='Head Of Department',background=mycolor1,font=myfont1)

        self.t1 = Entry(self.window,font=myfont1)
        self.t2 = Entry(self.window,font=myfont1)
        # ------------------ table ---------------------
        self.mytable1 = Treeview(self.window, columns=['c1', 'c2'], height=10)

        self.mytable1.heading('c1', text='Department')
        self.mytable1.heading('c2', text='Head Of Department')
        self.mytable1['show'] = 'headings'

        self.mytable1.column('c1', width=300, anchor='center')
        self.mytable1.column('c2', width=300, anchor='center')
        self.mytable1.bind("<ButtonRelease-1>",lambda e: self.getSelectedRow())

        #----------------- buttons ---------------------
        self.b1 = Button(self.window,text='Save',font=myfont1,background=mycolor2,command=self.saveData,borderwidth=2)
        self.b2 = Button(self.window,text='Update',font=myfont1,background=mycolor2,command=self.updateData,borderwidth=2)
        self.b3 = Button(self.window,text='Delete',font=myfont1,background=mycolor2,command=self.deleteData,borderwidth=2)
        self.b4 = Button(self.window,text='Fetch',font=myfont1,background=mycolor2,command=self.fetchData,borderwidth=2)
        self.b5 = Button(self.window,text='Search',font=myfont1,background=mycolor2,command=self.showAllData,borderwidth=2)

        # ------------placement -----------------
        self.hdlbl.place(x=0,y=0,width=w,height=70)
        x1 = 10
        y1 =100
        x_diff = 150
        y_diff = 50

        self.L1.place(x=x1,y=y1)
        self.t1.place(x=x1+x_diff+20,y=y1)
        self.b4.place(x=x1+x_diff*2+80,y=y1,width=100,height=25)
        self.mytable1.place(x=x1+x_diff*3+100,y=y1)
        y1+=y_diff
        self.L2.place(x=x1,y=y1)
        self.t2.place(x=x1+x_diff+20,y=y1)
        self.b5.place(x=x1+x_diff*2+80,y=y1,width=100,height=25)
        y1+=y_diff

        y1+=y_diff
        self.b1.place(x=x1,y=y1,width=150,height=40)
        self.b2.place(x=x1+x_diff,y=y1,width=150,height=40)
        self.b3.place(x=x1+x_diff*2,y=y1,width=150,height=40)


        #------call required functions ----------
        self.databaseConnection()

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
            #dname	hod
            qry = 'insert into department values (%s,%s)'
            rowcount = self.curr.execute(qry ,(self.t1.get(), self.t2.get()) )
            self.conn.commit()
            if rowcount==1:
                messagebox.showinfo("Success","Department Record Saved successfully",parent=self.window)
                self.clearPage()
            else:
                messagebox.showwarning("Failure","Department Record not Saved y",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in insertion : \n"+str(e),parent=self.window)

    def updateData(self):
        if self.validationCheck()==False:
            return # end this function now
        try:
            qry = 'update department set hod=%s where dname=%s'
            rowcount = self.curr.execute(qry ,( self.t2.get(), self.t1.get()) )
            self.conn.commit()
            if rowcount==1:

                messagebox.showinfo("Success","Department Record Updated successfully",parent=self.window)
                self.clearPage()
            else:
                messagebox.showwarning("Failure","Department Record not Updated ",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in insertion : \n"+str(e),parent=self.window)

    def deleteData(self):
        ans = messagebox.askquestion("Confirmation","Are you sure to delete??",parent=self.window)
        if ans=='yes':
            try:
                qry = 'delete from department  where dname=%s'
                rowcount = self.curr.execute(qry ,(self.t1.get()) )
                self.conn.commit()
                if rowcount==1:
                    messagebox.showinfo("Success","Department Record Deleted successfully",parent=self.window)
                    self.clearPage()
                else:
                    messagebox.showwarning("Failure","Department Record not Deleted ",parent=self.window)
            except Exception as e:
                messagebox.showerror("Query Error","Error in insertion : \n"+str(e),parent=self.window)

    def getSelectedRow(self):
        id = self.mytable1.focus()
        # print("Id of Selected Row = ",id)
        row_record = self.mytable1.item(id)
        # print("Row Record = ",row_record)
        row = row_record['values']
        # print("row = ",row)
        col0 = row[0]
        # print("col 0 = ",col0)
        self.fetchData(col0)

    def fetchData(self,pcolumn=None):
        if pcolumn==None:
            rollno  = self.t1.get()
        else:
            rollno = pcolumn
        try:
            #rollno	name	phone	gender	dob	address	department	course
            qry = 'select * from department where dname=%s'
            rowcount = self.curr.execute(qry ,(rollno) )
            rowdata = self.curr.fetchone()
            # print("Row Data = ",rowdata)
            self.clearPage()
            if rowdata:
                # set data in fields
                self.t1.insert(0,rowdata[0])
                self.t2.insert(0,rowdata[1])

            else:
                messagebox.showwarning("Empty","No Record Found",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in fetching : \n"+str(e),parent=self.window)

    def clearPage(self):
        self.t1.delete(0,END)
        self.t2.delete(0,END)
        self.showAllData()

    def showAllData(self):
        try:
            self.mytable1.delete(*self.mytable1.get_children())
            qry = 'select * from department where hod like %s'
            rowcount = self.curr.execute(qry,(self.t2.get()+"%") )
            rowdata = self.curr.fetchall()
            if rowdata:
                for row in rowdata:
                    self.mytable1.insert('',END,values=row)
            else:
                messagebox.showwarning("Empty","No Record Found",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in fetching : \n"+str(e),parent=self.window)

    def validationCheck(self):
        if len(self.t1.get())<2:
            messagebox.showwarning("Validation","Please Enter Department Name",parent=self.window)
            return False
        elif len(self.t2.get())<2:
            messagebox.showwarning("Validation","Please Enter Head of Department",parent=self.window)
            return False
        return True



#--------- for testing only ------------
if __name__ == '__main__':
    dummy_home=Tk()
    DepartmentClass(dummy_home)
    dummy_home.mainloop()