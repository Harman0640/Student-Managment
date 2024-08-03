import os
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview
import pymysql

from printoutpage import my_cust_PDF


class Report2Class:
    def __init__(self,hwindow):
        self.window = Toplevel(hwindow)
        self.window.title("My College Manager\Student Report")

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
        mycolor2 = '#E3E1D9'
        myfont1 = ('Cambria',13,'bold')
        self.window.config(background=mycolor1)

        self.hdlbl = Label(self.window,text='Student Report',background='grey',font=('Cambria',20,'bold'))

        self.v2 = StringVar()
        self.c1 = Combobox(self.window,textvariable=self.v2,font=myfont1,state='readonly')
        self.c1.bind("<<ComboboxSelected>>",lambda e: self.showAllData())
        #------------------ table ---------------------
        self.mytable1 = Treeview(self.window,columns=['c1','c2','c3','c4','c5','c6','c7','c8'],height=20)

        self.mytable1.heading('c1',text='Roll no')
        self.mytable1.heading('c2',text='Name')
        self.mytable1.heading('c3',text='Phone')
        self.mytable1.heading('c4',text='Gender')
        self.mytable1.heading('c5',text='DOB')
        self.mytable1.heading('c6',text='Address')
        self.mytable1.heading('c7',text='Department')
        self.mytable1.heading('c8',text='Course')
        self.mytable1['show']='headings'

        self.mytable1.column('c1',width=100,anchor='n')
        self.mytable1.column('c2',width=200,anchor='s')
        self.mytable1.column('c3',width=100,anchor='e')
        self.mytable1.column('c4',width=100,anchor='w')
        self.mytable1.column('c5',width=100,anchor='center')
        self.mytable1.column('c6',width=200,anchor='center')
        self.mytable1.column('c7',width=200,anchor='center')
        self.mytable1.column('c8',width=200,anchor='center')

        #----------------- buttons ---------------------
        self.b1 = Button(self.window,text='Print',font=myfont1,background=mycolor2, borderwidth=3,command=self.getPrintout)

        # ------------placement -----------------
        self.hdlbl.place(x=0,y=0,width=w,height=70)
        x1 = 40
        y1 =100
        x_diff = 150
        y_diff = 50
        self.c1.place(x=x1,y=y1)
        y1+=y_diff
        self.mytable1.place(x=x1,y=y1)
        y1+=450
        self.b1.place(x=x1+520,y=y1,width=150,height=40)

        #------call required functions ----------
        self.databaseConnection()
        self.getAllDepartments()
        self.pdata=[]
        self.window.mainloop()

    def getPrintout(self):
        pdf = my_cust_PDF()

        headings = ['Rollno', 'Name', 'Phone No', 'Gender', 'DOB', 'Address', 'Department', 'Course']

        pdf.page_content(headings, self.pdata)
        pdf.output('pdf_file1.pdf')
        os.system('explorer.exe "pdf_file1.pdf"')

    def databaseConnection(self):

        try:
            self.conn = pymysql.connect(host='localhost',db='mycollegemanger_db',user='root',password='')
            self.curr = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Connection Error","Error in Database Connection : \n"+str(e),parent=self.window)

    def showAllData(self):
        try:
            self.mytable1.delete(*self.mytable1.get_children())
            #rollno	name	phone	gender	dob	address	department	course
            qry = 'select * from student where department=%s'
            rowcount = self.curr.execute(qry ,self.v2.get())
            rowdata = self.curr.fetchall()
            # print("Row Data = ",rowdata)
            self.pdata=[]
            if rowdata:
                for row in rowdata:
                    myr1 = [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]]
                    self.mytable1.insert('',END,values=row)
                    self.pdata.append(myr1)
            else:
                messagebox.showwarning("Empty","No Record Found",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error in fetching : \n"+str(e),parent=self.window)

    def getAllDepartments(self):
        try:
            qry = 'select * from department'
            rowcount = self.curr.execute(qry)
            rowdata = self.curr.fetchall()
            self.dept_list = []
            if rowdata:
                self.c1.set("Choose Department")
                for row in rowdata:
                    self.dept_list.append(row[0])
            else:
                self.c1.set("No Department")
            self.c1.config(values=self.dept_list)

        except Exception as e:
            messagebox.showerror("Query Error", "Error in fetching : \n" + str(e), parent=self.window)
#--------- for testing only ------------
if __name__ == '__main__':
    dummy_home=Tk()
    Report2Class(dummy_home)
    dummy_home.mainloop()