from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import tkinter.messagebox
import os
import sqlite3
from turtle import bgcolor


#####################################################################################################################################################################################
class sis(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        all_frame = tk.Frame(self)
        all_frame.pack(side="top", fill="both", expand = True)
        all_frame.rowconfigure(0, weight=1)
        all_frame.columnconfigure(0, weight=1)
        self.frames = {}
        for F in (Students, Home, Courses):
            frame = F(all_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show(Home)
    def show(self, page_number):
        frame = self.frames[page_number]
        frame.tkraise()

#####################################################################################################################################################################################

def iExit():
            iExit = tkinter.messagebox.askyesno(" VIPC Student Information System","Confirm if you want to exit")
            if iExit > 0:
                root.destroy()
                return
class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        label = tk.Label(self, text="  VINEYARD  INTERNATIONAL \n POLYTECHNIC COLLEGE  \n \n \n STUDENT INFORMATION SYSTEM",borderwidth=8, relief="ridge", font=("Courier", 40), bg=("darkslategray"), fg=("white"))
        label.place(x=0,y=5,width=920,height=650)

        label = tk.Label(self, text="VIPC", borderwidth=8, relief="raised", font=("Algerian", 29), bg=("lightslategray"), fg=("lightslategray"))
        label.place(x=920,y=5,width=562,height=660)

    
        
        course = tk.Button(self, text="COURSES",font=("Courier",20),bd=5, width = 13, height = 1, fg="white",bg="darkslategray", relief='ridge', command=lambda: controller.show(Courses))
        course.place(x=1000,y=220)
        course.config(cursor= "hand2")
        
        students = tk.Button(self, text="REGISTRATION",font=("Courier",20),bd=5, width = 13 , height = 1, fg="white",bg="darkslategray",relief='ridge', command=lambda: controller.show(Students))
        students.place(x=1000,y=350)
        students.config(cursor= "hand2")

        students = tk.Button(self, text="EXIT",font=("Courier",20),bd=5, width = 13, height = 1, fg="white",bg="darkslategray",relief='ridge', command=iExit)
        students.place(x=1000,y=480)
        students.config(cursor= "hand2")

        
        
  #####################################################################################################################################################################################      

class Courses(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("VIPC Student Information System")
        
    
        Course_Code = StringVar()
        Course_Name = StringVar()
        SearchBar_Var = StringVar()
        
        def tablec():
            conn = sqlite3.connect("sis_v2.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS courses (Course_Code TEXT PRIMARY KEY, Course_Name TEXT)") 
            conn.commit() 
            conn.close()
            
        def add_course():
            if Course_Code.get() == "" or Course_Name.get() == "" : 
                tkinter.messagebox.showinfo("VIPC SIS", "Fill in student information")
            else:
                conn = sqlite3.connect("sis_v2.db")
                c = conn.cursor()         
                c.execute("INSERT INTO courses(Course_Code,Course_Name) VALUES (?,?)",(Course_Code.get(),Course_Name.get()))        
                conn.commit()           
                conn.close()
                Course_Code.set('')
                Course_Name.set('') 
                tkinter.messagebox.showinfo("VIPC SIS", "Registered Successfully!")
                display_course()
              
        def display_course():
            self.course_list.delete(*self.course_list.get_children())
            conn = sqlite3.connect("sis_v2.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            for row in rows:
                self.course_list.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
        
        def update_course():
            for selected in self.course_list.selection():
                conn = sqlite3.connect("sis_v2.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE courses SET Course_Code=?, Course_Name=? WHERE Course_Code=?", (Course_Code.get(),Course_Name.get(), self.course_list.set(selected, '#1')))  
                conn.commit()
                tkinter.messagebox.showinfo("VIPC SIS", "Updated Successfully!")
                display_course()
                clear()
                conn.close()
                
        def edit_course():
            x = self.course_list.focus()
            if x == "":
                tkinter.messagebox.showerror("VIPC SIS", "Please select a course")
                return
            values = self.course_list.item(x, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])
                    
        def delete_course(): 
            try:
                messageDelete = tkinter.messagebox.askyesno("VIPC SIS", "Are you sure you want to delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("sis_v2.db")
                    cur = con.cursor()
                    x = self.course_list.selection()[0]
                    id_no = self.course_list.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("DELETE FROM courses WHERE Course_Code = ?",(id_no,))                   
                    con.commit()
                    self.course_list.delete(x)
                    tkinter.messagebox.showinfo("VIPC SIS", "Deleted Successfully!")
                    display_course()
                    con.close()                    
            except:
                tkinter.messagebox.showerror("SIS", "This course has students!")
                
        def search_course():
            Course_Code = SearchBar_Var.get()                
            con = sqlite3.connect("sis_v2.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM courses WHERE Course_Code = ?",(Course_Code,))
            con.commit()
            self.course_list.delete(*self.course_list.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.course_list.insert("", tk.END, text=row[0], values=row[0:])
            con.close()

        def iExit():
            iExit = tkinter.messagebox.askyesno(" VIPC Student Information System","Confirm if you want to exit")
            if iExit > 0:
                root.destroy()
                return
        def clear():
            Course_Code.set('')
            Course_Name.set('') 
            
        def OnDoubleclick(event):
            item = self.course_list.selection()[0]
            values = self.course_list.item(item, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])

      

        home = tk.Button(self, text="HOME",font=("Lucida Console",13,"bold"),bd=0, width = 16, bg="darkslategray", fg="white", command=lambda: controller.show(Home))
        home.place(x=7,y=20, height=35)
        home.config(cursor= "hand2")

        students = tk.Button(self, text="REGISTRATION",font=("Lucida Console",13,"bold"),bd=0, width = 16 , fg="white",bg="darkslategray",command=lambda: controller.show(Students))
        students.place(x=1090,y=20, height=35)
        students.config(cursor= "hand2")

         #main color for the home page
        label = tk.Label(self, text="COURSES", font=("Times New Roman", 40),bg=("darkslategray"))
        label.place(x=200,y=20,width=880,height=650)
        

        ## side by side border for home page 
        label = tk.Label(self, text="VIPC", font=("Algerian", 29), bg=("lightslategray"), fg=("lightslategray"))
        label.place(x=10,y=60,width=180,height=670)
        
        label = tk.Label(self, text="VIPC", font=("Algerian", 29), bg=("lightslategray"), fg=("lightslategray"))
        label.place(x=1090,y=60,width=180,height=670)

       
        
        ##top title frame
        self.lblccode = Label(self, font=("Times New Roman", 30, "bold"),bd=5,bg=("lightslategray"),fg=("white"),text="VIPC COURSES", padx=2, pady=4)
        self.lblccode.place(x=200,y=20,width=880)

      

        self.lblccode = Label(self, font=("Lucida Console", 12, "bold"),bg=("darkslategray"),fg=("white"),text="Course Code:", padx=4, pady=4)
        self.lblccode.place(x=350,y=150)
        self.txtccode = Entry(self, font=("Lucida Console", 12, "bold"), textvariable=Course_Code,bd=0, bg="white", width=25)
        self.txtccode.place(x=540,y=150, height=25) 

        self.lblccode = Label(self, font=("Lucida Console", 12, "bold"),bg=("darkslategray"),fg=("white"),text=" Course Code:", padx=4, pady=4)
        self.lblccode.place(x=340,y=100)



        self.lblcname = Label(self, font=("Lucida Console", 12,"bold"),bg=("darkslategray"),fg=("white"), text=" Course Name:", padx=4, pady=4)
        self.lblcname.place(x=340,y=200)
        self.txtcname = Entry(self, font=("Lucida Console", 12, "bold"), textvariable=Course_Name,bd=0,bg="white", width=25)
        self.txtcname.place(x=540,y=200, height=25)
        
        self.SearchBar = Entry(self, font=("Lucida Console", 12), textvariable=SearchBar_Var, bd=0,bg="white",width=27)
        self.SearchBar.place(x=540,y=100, height=25)


       
        ##Scroll bar positioning for home page
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=980,y=250,height=390)

        self.course_list = ttk.Treeview(self, columns=("Course Code","Course Name"), height = 18, yscrollcommand=scrollbar.set)

        self.course_list.heading("Course Code", text="Course Code", anchor=W)
        self.course_list.heading("Course Name", text="Course Name",anchor=W)
        self.course_list['show'] = 'headings'

        self.course_list.column("Course Code",width=200, anchor=W, stretch=False)
        self.course_list.column("Course Name",width=430, stretch=False)
        
        self.course_list.bind("<Double-1> ", OnDoubleclick)

       ## Treeview for course
        self.course_list.place(x=330,y=250)
        scrollbar.config(command=self.course_list.yview)
            
        ## Buttons

        self.adds = Button(self, text="ADD", font=('Courier', 16, 'bold'), bd=5, height=1, width=10,bg="darkslategray", fg="white",relief='ridge',command=add_course)
        self.adds.place(x=25,y=350)
        self.adds.config(cursor= "hand2")


        self.clear = Button(self, text="CLEAR", font=('Courier', 16, 'bold'),bd=5, height=1, width=10, bg="darkslategray", fg="white",relief='ridge', command=clear)
        self.clear.place(x=25,y=430)
        self.clear.config(cursor= "hand2")

        self.search = Button(self, text="SEARCH", font=('Courier', 9, 'bold'),bd=3, height=1, width=12, bg= "lightslategray", fg="darkslategray",relief='ridge', command=search_course)
        self.search.place(x=820,y=98)
        self.search.config(cursor= "hand2")

        self.display = Button(self, text="DISPLAY", font=('Courier', 16, 'bold'),bd=5, height=1, width=10, bg="darkslategray", fg="white",relief='ridge', command=display_course)
        self.display.place(x=25,y=510)
        self.display.config(cursor= "hand2")

        
        self.delete = Button(self, text="DELETE", font=('Courier', 16, 'bold'),bd=5, height=1, width=10, bg="darkslategray", fg="white",relief='ridge', command=delete_course)
        self.delete.place(x=1110,y=350)
        self.delete.config(cursor= "hand2")

        self.edit = Button(self, text="EDIT", font=('Courier', 16, 'bold'),bd=5, height=1, width=10, bg="darkslategray", fg="white",relief='ridge', command=edit_course)
        self.edit.place(x=1110,y=430)
        self.edit.config(cursor= "hand2")

        self.update = Button(self, text="UPDATE", font=('Courier', 16, 'bold'),bd=5, height=1, width=10, bg="darkslategray", fg="white",relief='ridge', command=update_course) 
        self.update.place(x=1110,y=510)
        self.update.config(cursor= "hand2")
        
        tablec()
        display_course()

#####################################################################################################################################################################################

class Students(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.controller.title("VIPC Student Information System")
        
        
      

        #main color for the home page
        label = tk.Label(self, text="COURSES", font=("Times New Roman", 40),bg=("darkslategray"),fg=("darkslategray"))
        label.place(x=0,y=10,width=1280,height=650)

        ## side by side border for home page 
        label = tk.Label(self, text="VPIC", font=("Algerian", 29), bg=("lightslategray"), fg=("lightslategray"))
        label.place(x=10,y=60,width=180,height=670)
        
        label = tk.Label(self, text="VPIC", font=("Algerian", 29), bg=("lightslategray"), fg=("lightslategray"))
        label.place(x=1090,y=60,width=180,height=670)

         ##top title frame
        self.lblccode = Label(self, font=("Times New Roman", 30, "bold"),bd=5,bg=("darkslategray"),fg=("white"),text="VIPC REGISTRATION FORM", padx=2, pady=4)
        self.lblccode.place(x=200,y=20,width=880)

        course = tk.Button(self, text="COURSES",font=("Lucida Console",13,"bold"),bd=0, width = 16, fg="white",bg="lightslategray", command=lambda: controller.show(Courses))
        course.place(x=7,y=20,height=35)
        course.config(cursor= "hand2")

        home = tk.Button(self, text="HOME",font=("Lucida Console",13,"bold"),bd=0, width = 16, bg="lightslategray", fg="white", command=lambda: controller.show(Home))
        home.place(x=1090,y=20, height=35)
        home.config(cursor= "hand2")



        

        
        Student_ID = StringVar()
        Student_Name = StringVar()       
        Student_YearLevel = StringVar()
        Student_Gender = StringVar()
        Course_Code = StringVar()
        SearchBar_Var = StringVar()
        

        def tables():
            conn = sqlite3.connect("sis_v2.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS students (Student_ID TEXT PRIMARY KEY, Student_Name TEXT, Course_Code TEXT, \
                      Student_YearLevel TEXT, Student_Gender TEXT, \
                      FOREIGN KEY(Course_Code) REFERENCES courses(Course_Code) ON UPDATE CASCADE)") 
            conn.commit() 
            conn.close()    
        
        def add_stud():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("VIPC SIS", "Fill in student information")
            else:  
                ID = Student_ID.get()
                ID_list = []
                for i in ID:
                    ID_list.append(i)
                a = ID.split("-")
                if len(a[0]) == 4:        
                    if "-" in ID_list:
                        if len(a[1]) == 1:
                            tkinter.messagebox.showerror("SIS", "ID Format:YYYY-NNNN")
                        elif len(a[1]) ==2:
                            tkinter.messagebox.showerror("SIS", "ID Format:YYYY-NNNN")
                        elif len(a[1]) ==3:
                            tkinter.messagebox.showerror("SIS", "ID Format:YYYY-NNNN")
                        else:
                            x = ID.split("-")  
                            year = x[0]
                            number = x[1]
                            if year.isdigit()==False or number.isdigit()==False:
                                try:
                                    tkinter.messagebox.showerror("VIPC SIS", "Invalid ID")
                                except:
                                    pass
                            elif year==" " or number==" ":
                                try:
                                    tkinter.messagebox.showerror("VIPC SIS", "Invalid ID")
                                except:
                                    pass
                            else:
                                try:
                                    conn = sqlite3.connect("sis_v2.db")
                                    c = conn.cursor() 
                                    c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                                    c.execute("INSERT INTO students(Student_ID,Student_Name,Course_Code,Student_YearLevel,Student_Gender) VALUES (?,?,?,?,?)",\
                                                          (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get()))                                       
                                                                       
                                    tkinter.messagebox.showinfo("VIPC SIS", "Added Successfully!")
                                    conn.commit() 
                                    clear()
                                    display_stud()
                                    conn.close()
                                except:
                                    ids=[]
                                    conn = sqlite3.connect("sis_v2.db")
                                    c = conn.cursor()
                                    c.execute("SELECT * FROM students")
                                    rows = c.fetchall()
                                    for row in rows:
                                        ids.append(row[0])
                                    if ID in ids:
                                       tkinter.messagebox.showerror("VIPC SIS", "ID already exists")
                                    else: 
                                       tkinter.messagebox.showerror("VIPC SIS", "Course Unavailable")
                                   
                    else:
                        tkinter.messagebox.showerror("VIPC SIS", "Invalid ID")
                else:
                    tkinter.messagebox.showerror("VIPC SIS", "Invalid ID")
                 
        def update_stud():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("VIPC SIS", "Select a student")
            else:
                for selected in self.studentlist.selection():
                    conn = sqlite3.connect("sis_v2.db")
                    cur = conn.cursor()
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("UPDATE students SET Student_ID=?, Student_Name=?, Course_Code=?, Student_YearLevel=?,Student_Gender=?\
                          WHERE Student_ID=?", (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get(),\
                              self.studentlist.set(selected, '#1')))
                    conn.commit()
                    tkinter.messagebox.showinfo("VIPC SIS", "Updated Successfully!")
                    display_stud()
                    clear()
                    conn.close()
        
        def delete_stud():   
            try:
                messageDelete = tkinter.messagebox.askyesno("VIPC SIS", "Are you sure you want to permanently delete this?")
                if messageDelete > 0:   
                    con = sqlite3.connect("sis_v2.db")
                    cur = con.cursor()
                    x = self.studentlist.selection()[0]
                    id_no = self.studentlist.item(x)["values"][0]
                    cur.execute("DELETE FROM students WHERE Student_ID = ?",(id_no,))                   
                    con.commit()
                    self.studentlist.delete(x)
                    tkinter.messagebox.showinfo("VIPC SIS", "Deleted Successfully!")
                    display_stud()
                    clear()
                    con.close()                    
            except Exception as e:
                print(e)
                
        def search_stud():
            Student_ID = SearchBar_Var.get()
            try:  
                con = sqlite3.connect("sis_v2.db")
                cur = con.cursor()
                cur .execute("PRAGMA foreign_keys = ON")
                cur.execute("SELECT * FROM students")
                con.commit()
                self.studentlist.delete(*self.studentlist.get_children())
                rows = cur.fetchall()
                for row in rows:
                    if row[0].startswith(Student_ID):
                        self.studentlist.insert("", tk.END, text=row[0], values=row[0:])
                con.close()
            except:
                tkinter.messagebox.showerror("VIPC SIS", "Invalid ID")           
                
        def display_stud():
            self.studentlist.delete(*self.studentlist.get_children())
            conn = sqlite3.connect("sis_v2.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM students")
            rows = cur.fetchall()
            for row in rows:
                self.studentlist.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
                            
        def edit_stud():
            x = self.studentlist.focus()
            if x == "":
                tkinter.messagebox.showerror("VIPC SIS", "Select student record")
                return
            values = self.studentlist.item(x, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])
        
        def clear():
            Student_ID.set('')
            Student_Name.set('') 
            Student_YearLevel.set('')
            Student_Gender.set('')
            Course_Code.set('')
            
        def OnDoubleClick(event):
            item = self.studentlist.selection()[0]
            values = self.studentlist.item(item, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])
        

        self.lblid = Label(self, font=("Lucida Console", 12,"bold"),bg="darkslategray",fg="white", text="ID Number:", padx=4, pady=4)
        self.lblid.place(x=220,y=250)
        self.txtid = Entry(self, font=("Lucida Console", 13), textvariable=Student_ID, width=16)
        self.txtid.place(x=220,y=300,height=25)

        self.lblname = Label(self, font=("Lucida Console", 12,"bold"),bg="darkslategray",fg="white", text="Student Name:", padx=4, pady=4)
        self.lblname.place(x=350,y=150)
        self.txtname = Entry(self, font=("Lucida Console", 12), textvariable=Student_Name, width=25)
        self.txtname.place(x=559,y=150,height=25)
        
        self.lblc = Label(self, font=("Lucida Console", 12,"bold"),bg="darkslategray",fg="white", text="Course Code:", padx=4, pady=4)
        self.lblc.place(x=220,y=350)
        self.txtyear = ttk.Combobox(self, value=["BS STAT", "BS MATH", "BSIT", "BSCS","BSA","BS BIO","BS CHEM","BSCE","BSHM","BSME","BSN","BA Hist","BSEE","BA POLSCI", "BSBA EM", "BSHRM","BSMB", "BST","BSFM"], state="readonly", font=("Lucida Console", 12), textvariable=Course_Code, width=15)
        self.txtyear.place(x=220,y=400,height=25)
        

        self.lblyear = Label(self, font=("Lucida Console", 12,"bold"),bg="darkslategray",fg="white", text="Year Level:", padx=4, pady=4)
        self.lblyear.place(x=220,y=450)
        self.txtyear = ttk.Combobox(self, value=["1st Year", "2nd Year", "3rd Year", "4th Year"], state="readonly", font=("Times New Roman", 13), textvariable=Student_YearLevel, width=16)
        self.txtyear.place(x=220,y=500,height=25)
        
        self.lblgender = Label(self, font=("Times New Roman", 13,"bold"),bg="darkslategray",fg="white", text="Gender:", padx=4, pady=4)
        self.lblgender.place(x=220,y=550)
        self.txtgender = ttk.Combobox(self, value=["Male", "Female"], font=("Lucida Console", 13), state="readonly", textvariable=Student_Gender, width=15)
        self.txtgender.place(x=220,y=600,height=25)

        self.SearchBar = Entry(self, font=("Lucida Console", 12), textvariable=SearchBar_Var, bd=0,bg="white", width=25)
        self.SearchBar.place(x=560,y=100, height=25)

        self.lblccode = Label(self, font=("Lucida Console", 12, "bold"),bg=("darkslategray"),fg=("white"),text=" Student ID Number:", padx=4, pady=4)
        self.lblccode.place(x=340,y=100)

        ## Treeview
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1050,y=250,height=390)

        self.studentlist = ttk.Treeview(self, columns=("ID Number", "Name", "Course", "Year Level", "Gender"), height = 18, yscrollcommand=scrollbar.set)

        self.studentlist.heading("ID Number", text="ID Number", anchor=W)
        self.studentlist.heading("Name", text="Name",anchor=W)
        self.studentlist.heading("Course", text="Course",anchor=W)
        self.studentlist.heading("Year Level", text="Year Level",anchor=W)
        self.studentlist.heading("Gender", text="Gender",anchor=W)
        self.studentlist['show'] = 'headings'

        self.studentlist.column("ID Number", width=100, anchor=W, stretch=False)
        self.studentlist.column("Name", width=200, stretch=False)
        self.studentlist.column("Course", width=130, anchor=W, stretch=False)
        self.studentlist.column("Year Level", width=100, anchor=W, stretch=False)
        self.studentlist.column("Gender", width=100, anchor=W, stretch=False)
        
        self.studentlist.bind("<Double-1>",OnDoubleClick)
        
        

        self.studentlist.place(x=400,y=250)
        scrollbar.config(command=self.studentlist.yview)
        
        ## Buttons
        
        self.add = Button(self, text="REGISTER", font=('Courier', 16,'bold'), height=1, width=10, bd=5,  bg="darkslategray", fg="white", relief='ridge',command=add_stud)
        self.add.place(x=25,y=350)
        self.add.config(cursor= "hand2")

        self.update = Button(self, text="UPDATE", font=('Courier', 16,'bold'), height=1, width=10, bd=5, bg="darkslategray", fg="white",relief='ridge', command=update_stud)
        self.update.place(x=1110,y=510)
        self.update.config(cursor= "hand2")

        self.clear = Button(self, text="CLEAR", font=('Courier', 16,'bold'), height=1, width=10, bd=5, bg="darkslategray", fg="white",relief='ridge', command=clear)
        self.clear.place(x=25,y=430)
        self.clear.config(cursor= "hand2")

        self.delete = Button(self, text="DELETE", font=('Courier', 16,'bold'), height=1, width=10, bd=5, bg="darkslategray", fg="white",relief='ridge', command=delete_stud)
        self.delete.place(x=1110,y=350)
        self.delete.config(cursor= "hand2")

        self.search = Button(self, text="SEARCH", font=('Courier', 9, 'bold'),bd=3,height=1, width=12, bg= 'lightslategray', fg="white",relief='ridge', command=search_stud)
        self.search.place(x=820,y=98)
        self.search.config(cursor= "hand2")

        self.display = Button(self, text="DISPLAY", font=('Courier', 16, 'bold'), height=1, width=10,bd=5,  bg="darkslategray", fg="white", relief='ridge',command = display_stud)
        self.display.place(x=25,y=510)
        self.display.config(cursor= "hand2")

        self.edit = Button(self, text="EDIT", font=('Courier', 16, 'bold'),bd=5, height=1, width=10, bg="darkslategray", fg="white",relief='ridge', command= edit_stud)
        self.edit.place(x=1110,y=430)
        self.edit.config(cursor= "hand2")

        tables()
        display_stud()

#####################################################################################################################################################################################

root = sis()
root.geometry("1260x600")

root.mainloop()
