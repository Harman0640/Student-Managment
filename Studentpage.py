from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Treeview
import pymysql
from tkcalendar import DateEntry
from PIL import Image,ImageTk

class StudentClass:
    defaultname="default_image.png"


    def __init__(self,hwindow):
        self.window = Toplevel(hwindow)
        self.window.title("My College Manager\Student")

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
        myfont1 = ('Cambria','13','bold')
        self.window.config(background=mycolor1)

        self.hdlbl = Label(self.window, text='Information', background="grey", font=('Cambria', 20, 'bold'))


        self.L1 = Label(self.window,text='Roll no',background=mycolor1,font=myfont1)
        self.L2 = Label(self.window,text='Name',background=mycolor1,font=myfont1)
        self.L3 = Label(self.window,text='Phone',background=mycolor1,font=myfont1)
        self.L4 = Label(self.window,text='Gender',background=mycolor1,font=myfont1)
        self.L5 = Label(self.window,text='DOB',background=mycolor1,font=myfont1)
        self.L6 = Label(self.window,text='Address',background=mycolor1,font=myfont1)
        self.L7 = Label(self.window,text='Department',background=mycolor1,font=myfont1)
        self.L8 = Label(self.window,text='Course',background=mycolor1,font=myfont1)

        self.t1 = Entry(self.window,font=myfont1,width=20,borderwidth=4)
        self.t2 = Entry(self.window,font=myfont1,borderwidth=4)
        self.t3 = Entry(self.window,font=myfont1,borderwidth=4)
        self.v1 = StringVar()
        self.r1 = Radiobutton(self.window,text='Male',value='Male',variable=self.v1,background=mycolor1,font=myfont1)
        self.r2 = Radiobutton(self.window,text='Female',value='Female',variable=self.v1,background=mycolor1,font=myfont1)
        self.t5 =  DateEntry(self.window,  background='gray',width=12,
                    foreground='white', borderwidth=2, year=2000,date_pattern='y-mm-dd')
        self.t6 = Text(self.window,font=myfont1,width=35,height=3,borderwidth=4)
        self.v2 = StringVar()
        self.c1 = Combobox(self.window,textvariable=self.v2,font=myfont1, values=['IT','SCIENCE','MECHANICAL'],state='readonly')
        self.c1.bind("<<ComboboxSelected>>",lambda e: self.getAllCourses())

        self.v3 = StringVar()
        self.c2 = Combobox(self.window,textvariable=self.v3,font=myfont1,values=['BCA', 'B.TECH', 'MCA'],state='readonly')

        # ------------------ table ---------------------
        self.mytable1 = Treeview(self.window, columns=['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8'], height=15)

        self.mytable1.heading('c1', text='Roll no')
        self.mytable1.heading('c2', text='Name')
        self.mytable1.heading('c3', text='Phone')
        self.mytable1.heading('c4', text='Gender')
        self.mytable1.heading('c5', text='DOB')
        self.mytable1.heading('c6', text='Address')
        self.mytable1.heading('c7', text='Department')
        self.mytable1.heading('c8', text='Course')
        self.mytable1['show'] = 'headings'

        self.mytable1.column('c1', width=100, anchor='center')
        self.mytable1.column('c2', width=100, anchor='center')
        self.mytable1.column('c3', width=100, anchor='center')
        self.mytable1.column('c4', width=100, anchor='center')
        self.mytable1.column('c5', width=100, anchor='center')
        self.mytable1.column('c6', width=100, anchor='center')
        self.mytable1.column('c7', width=100, anchor='center')
        self.mytable1.column('c8', width=100, anchor='center')
        self.mytable1.bind("<ButtonRelease-1>",lambda e: self.getSelectedRow())

        #----------------- buttons ---------------------
        self.b1 = Button(self.window,text='Save',font=myfont1,background=mycolor2, width=7,borderwidth=4,command=self.saveData)
        self.b2 = Button(self.window,text='Update',font=myfont1,background=mycolor2,width=7,borderwidth=4,command=self.updateData)
        self.b3 = Button(self.window,text='Delete',font=myfont1,background=mycolor2,width=7,borderwidth=4,command=self.deleteData)
        self.b4 = Button(self.window,text='Fetch',font=myfont1,background=mycolor2,width=7,borderwidth=4,command=self.fetchData)
        self.b5 = Button(self.window,text='Search',font=myfont1,background=mycolor2,width=7,borderwidth=4,command=self.showAllData)

        # ------------placement -----------------
        self.hdlbl.place(x=0,y=0,width=w,height=70)
        x1 = 10
        y1 =100
        x_diff = 150
        y_diff = 50

        self.L1.place(x=x1,y=y1)
        self.t1.place(x=x1+x_diff,y=y1)
        self.b4.place(x=x1+x_diff*2+70,y=y1,width=80,height=30)
        self.mytable1.place(x=x1+x_diff*3+70,y=y1)
        y1+=y_diff
        self.L2.place(x=x1,y=y1)
        self.t2.place(x=x1+x_diff,y=y1)
        self.b5.place(x=x1+x_diff*2+70,y=y1,width=80,height=30)
        y1+=y_diff
        self.L3.place(x=x1,y=y1)
        self.t3.place(x=x1+x_diff,y=y1)
        y1+=y_diff
        self.L4.place(x=x1,y=y1)
        self.r1.place(x=x1+x_diff,y=y1)
        self.r2.place(x=x1+x_diff+x_diff,y=y1)
        y1+=y_diff
        self.L5.place(x=x1,y=y1)
        self.t5.place(x=x1+x_diff,y=y1)
        y1+=y_diff
        self.L6.place(x=x1,y=y1)
        self.t6.place(x=x1+x_diff,y=y1)
        y1+=y_diff
        y1+=y_diff
        self.L7.place(x=x1,y=y1)
        self.c1.place(x=x1+x_diff,y=y1)
        y1+=y_diff
        self.L8.place(x=x1,y=y1)
        self.c2.place(x=x1+x_diff,y=y1)
        y1+=y_diff
        self.b1.place(x=x1,y=y1,width=150,height=40)
        self.b2.place(x=x1+x_diff+100,y=y1,width=150,height=40)
        self.b3.place(x=x1+x_diff*2+200,y=y1,width=150,height=40)

        #------call required functions ----------
        self.databaseConnection()
        self.getAllDepartments()
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
            #rollno	name	phone	gender	dob	address	department	course
            qry = 'insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            rowcount = self.curr.execute(qry ,(self.t1.get(), self.t2.get(),self.t3.get(),
                    self.v1.get(),self.t5.get_date(),self.t6.get('0.0',END).strip(),
                                               self.v2.get(),self.v3.get(),self.actualname) )
            self.conn.commit()
            if rowcount==1:

                messagebox.showinfo("Success","Student Record Saved successfully",parent=self.window)
                self.clearPage()
            else:
                messagebox.showwarning("Failure","Student Record not Saved y",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in insertion : \n"+str(e),parent=self.window)

    def updateData(self):
        if self.validationCheck()==False:
            return # end this function now
        try:
            #rollno	name	phone	gender	dob	address	department	course
            qry = 'update student set name=%s, phone=%s,gender=%s, dob=%s,' \
                  ' address=%s, department=%s,course=%s,pic = %s where rollno=%s'
            rowcount = self.curr.execute(qry ,( self.t2.get(),self.t3.get(),
                    self.v1.get(),self.t5.get_date(),self.t6.get('0.0',END).strip(),
                    self.v2.get(),self.v3.get(),self.actualname, self.t1.get()) )
            self.conn.commit()
            if rowcount==1:

                #-----------------------------------------------------------

                messagebox.showinfo("Success","Student Record Updated successfully",parent=self.window)
                self.clearPage()
            else:
                messagebox.showwarning("Failure","Student Record not Updated ",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in insertion : \n"+str(e),parent=self.window)

    def deleteData(self):
        ans = messagebox.askquestion("Confirmation","Are you sure to delete??",parent=self.window)
        if ans=='yes':
            try:
                #rollno	name	phone	gender	dob	address	department	course
                qry = 'delete from student  where rollno=%s'
                rowcount = self.curr.execute(qry ,(self.t1.get()) )
                self.conn.commit()
                if rowcount==1:

                    #-----------------------------------------------------------
                    messagebox.showinfo("Success","Student Record Deleted successfully",parent=self.window)
                    self.clearPage()
                else:
                    messagebox.showwarning("Failure","Student Record not Deleted ",parent=self.window)
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
            qry = 'select * from student where rollno=%s'
            rowcount = self.curr.execute(qry ,(rollno) )
            rowdata = self.curr.fetchone()
            # print("Row Data = ",rowdata)
            self.clearPage()
            if rowdata:
                # set data in fields
                self.t1.insert(0,rowdata[0])
                self.t2.insert(0,rowdata[1])
                self.t3.insert(0,rowdata[2])
                self.v1.set(rowdata[3])
                self.t5.set_date(rowdata[4])
                self.t6.insert('0.0',rowdata[5])
                self.v2.set(rowdata[6])
                self.v3.set(rowdata[7])

            else:
                messagebox.showwarning("Empty","No Record Found",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in fetching : \n"+str(e),parent=self.window)

    def clearPage(self):
        self.t1.delete(0,END)
        self.t2.delete(0,END)
        self.t3.delete(0,END)
        self.v1.set(None)
        self.t5.delete(0,END)
        self.t6.delete('0.0',END)
        self.c1.set("Choose Department")
        self.c2.set("Choose Course")
        self.showAllData()


    def showAllData(self):
        try:
            self.mytable1.delete(*self.mytable1.get_children())
            #rollno	name	phone	gender	dob	address	department	course
            qry = 'select * from student where name like %s'
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
        if not self.t1.get().isdigit():
            messagebox.showwarning("Validation","Please Enter Valid Rollno\n(only digits)",parent=self.window)
            return False
        elif len(self.t2.get())<2:
            messagebox.showwarning("Validation","Please Enter Proper Name\n(atleast 2 characters)",parent=self.window)
            return False
        elif not self.t3.get().isdigit() or len(self.t3.get())!=10:
            messagebox.showwarning("Validation","Please Enter Correct Phone Number \n(10 Digits)",parent=self.window)
            return False
        elif not(self.v1.get()=='Female' or self.v1.get()=='Male'):
            messagebox.showwarning("Validation","Please Select Gender",parent=self.window)
            return False
        elif self.t5.get()=="":
            messagebox.showwarning("Validation","Please Select DOB",parent=self.window)
            return False
        elif len(self.t6.get('0.0',END))<3:
            messagebox.showwarning("Validation","Please Enter Proper Address\n(atleast 3 characters)",parent=self.window)
            return False
        elif self.v2.get()=="Choose Department"  or self.v2.get()=="No Department":
            messagebox.showwarning("Validation","Please Select Department",parent=self.window)
            return False
        elif self.v3.get()=="Choose Course"  or self.v3.get()=="No Course":
            messagebox.showwarning("Validation","Please Select Course",parent=self.window)
            return False
        return True

    def getAllDepartments(self):
        try:
            qry = 'select * from department'
            rowcount = self.curr.execute(qry )
            rowdata = self.curr.fetchall()
            self.dept_list=[]
            if rowdata:
                self.c1.set("Choose Department")
                for row in rowdata:
                     self.dept_list.append(row[0])
            else:
                self.c1.set("No Department")
            self.c1.config(values=self.dept_list)

        except Exception as e:
            messagebox.showerror("Query Error","Error in fetching : \n"+str(e),parent=self.window)

    def getAllCourses(self):
        try:
            qry = 'select * from course where dname=%s'
            rowcount = self.curr.execute(qry,(self.v2.get()))
            rowdata = self.curr.fetchall()
            self.course_list = []
            if rowdata:
                self.c2.set("Choose Course")
                for row in rowdata:
                    self.course_list.append(row[1])
            else:
                self.c2.set("No Course")
            self.c2.config(values=self.course_list)

        except Exception as e:
            messagebox.showerror("Query Error", "Error in fetching : \n" + str(e), parent=self.window)

#--------- for testing only ------------
if __name__ == '__main__':
    dummy_home=Tk()
    StudentClass(dummy_home)
    dummy_home.mainloop()


class Studentclass:
    pass