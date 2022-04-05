
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import tkinter.ttk as ttk
import csv
import os


class Student:
    
    def __init__ (self,root):
        self.root = root
        blank_space = ""
        self.root.title(200 * blank_space + "      MSU-IIT Student Information System")
        self.root.geometry("1300x550+0+0")
    
        self.data = dict()
        self.temp = dict()
        self.filename = "Studentinfo.csv"
        
        Student_First_Name = StringVar()
        Student_Middle_Initial = StringVar()
        Student_Last_Name = StringVar()
        Student_IDNumber = StringVar()
        Student_YearLevel = StringVar()
        Student_Gender = StringVar()
        Student_Course = StringVar()
        searchbar = StringVar()
        
        if not os.path.exists('Studentinfo.csv'):
            with open('Studentinfo.csv', mode='w') as csv_file:
                fieldnames = ["Student ID Number", "Last Name", "First Name", "Middle Initial","Gender", "Year Level", "Course"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
        
        else:
            with open('Studentinfo.csv', newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    self.data[row["Student ID Number"]] = {'Last Name': row["Last Name"], 'First Name': row["First Name"], 'Middle Initial': row["Middle Initial"], 'Gender': row["Gender"],'Year Level': row["Year Level"], 'Course': row["Course"]}
            self.temp = self.data.copy()
        
        
         
        #=============================================================FUNCTIONS================================================================#
        
        def iExit():
            iExit = tkinter.messagebox.askyesno(" MSU-IIT Student Information System","Confirm if you want to exit")
            if iExit > 0:
                root.destroy()
                return
            
        def addStudent():
            with open('Studentinfo.csv', "a", newline="") as file:
                csvfile = csv.writer(file)
                if Student_IDNumber.get()=="" or Student_First_Name.get()=="" or Student_Middle_Initial.get()=="" or Student_Last_Name.get()=="" or Student_YearLevel.get()=="":
                    tkinter.messagebox.showinfo("SIS","Please fill in student information.")
                else:
                    self.data[Student_IDNumber.get()] = {'Last Name': Student_Last_Name.get(), 'First Name': Student_First_Name.get(), 'Middle Initial': Student_Middle_Initial.get(), 'Gender': Student_Gender.get(),'Year Level': Student_YearLevel.get(), 'Course': Student_Course.get()}
                    self.saveData()
                    tkinter.messagebox.showinfo("SIS", "Recorded Successfully!")
                Clear()
                displayData()
                    
        
        def Clear():
            Student_IDNumber.set("")
            Student_First_Name.set("")
            Student_Middle_Initial.set("")
            Student_Last_Name.set("")
            Student_YearLevel.set("")
            Student_Gender.set("")
            Student_Course.set("")

        
        
        def displayData():
            tree.delete(*tree.get_children())
            with open('Studentinfo.csv') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    IDNumber=row['Student ID Number']
                    LastName=row['Last Name']
                    FirstName=row['First Name']
                    MiddleInitial=row['Middle Initial']
                    YearLevel=row['Year Level']
                    Course=row['Course']
                    Gender=row['Gender']
                    tree.insert("",END, values=(IDNumber, LastName, FirstName, MiddleInitial, Gender, YearLevel, Course))
                    
      
        
        def deleteData():
            if tree.focus()=="":
                tkinter.messagebox.showerror("Student Information System","Please select student record from the list")
                return
            id_no = tree.item(tree.focus(),"values")[0]
            
            self.data.pop(id_no, None)
            self.saveData()
            tree.delete(tree.focus())
            tkinter.messagebox.showinfo("Student Information System","Student Record Deleted Successfully")
            
        
        
        def searchData():
            if self.searchbar.get() in self.data:
                vals = list(self.data[self.searchbar.get()].values())
                tree.delete(*tree.get_children())
                tree.insert("",0, values=(self.searchbar.get(), vals[0],vals[1],vals[2],vals[3],vals[4],vals[5]))
            elif self.searchbar.get() == "":
                displayData()
            else:
                tkinter.messagebox.showerror("Student Information System","Student not found")
                return
            
        
        
        
        def editData():
            if tree.focus() == "":
                tkinter.messagebox.showerror("Student Information System", "Please select student record from the list")
                return
            values = tree.item(tree.focus(), "values")
            Student_IDNumber.set(values[0])
            Student_Last_Name.set(values[1])
            Student_First_Name.set(values[2])
            Student_Middle_Initial.set(values[3])
            Student_Gender.set(values[4])
            Student_YearLevel.set(values[5])
            Student_Course.set(values[6])
       
    
       
        def updateData():
            with open('Studentinfo.csv', "a", newline="") as file:
                csvfile = csv.writer(file)
                if Student_IDNumber.get()=="" or Student_First_Name.get()=="" or Student_Middle_Initial.get()=="" or Student_Last_Name.get()=="" or Student_YearLevel.get()=="":
                    tkinter.messagebox.showinfo("SIS","Please select student record from the list")
                else:
                    self.data[Student_IDNumber.get()] = {'Last Name': Student_Last_Name.get(), 'First Name': Student_First_Name.get(), 'Middle Initial': Student_Middle_Initial.get(), 'Gender': Student_Gender.get(),'Year Level': Student_YearLevel.get(), 'Course': Student_Course.get()}
                    self.saveData()
                    tkinter.messagebox.showinfo("SIS", "Updated Successfully")
                Clear()
                displayData()     

        #============================================================FRAMES====================================================#
        
        MainFrame = Frame(self.root, bd=7, width=80, height=300, relief=GROOVE, bg="DARKSLATEGRAY")
        MainFrame.grid()
        
        BotFrame1 = Frame(MainFrame,  width=1300, height=100, relief=GROOVE,bg="DARKSLATEGRAY")
        BotFrame1.grid(row=4, column=0)

        BotFrame1 = Frame(MainFrame,  width=1300, height=200, relief=GROOVE,bg="DARKSLATEGRAY")
        BotFrame1.grid(row=2, column=0)
        
        TitleFrame = Frame(MainFrame, bg="LIGHTSLATEGRAY",bd=5, width=400, height=400, relief=GROOVE)
        TitleFrame.grid(row=0, column=0)
        
        TopFrame2 = Frame(MainFrame, bd=5,bg="LIGHTSLATEGRAY", width=500, height=450, relief=FLAT)
        TopFrame2.grid(row=3, column=0)
        
      
        LeftFrame = Frame(TopFrame2, bd=0, width=1200, height=400, padx=2, bg="LIGHTSLATEGRAY", relief=RAISED)
        LeftFrame.pack(side=LEFT)
        
        LeftFrame1 = Frame(LeftFrame, bd=0,bg="DARKSLATEGRAY", width=200, height=300, padx=2, pady=4, relief=FLAT)
        LeftFrame1.pack(side=TOP, padx=0, pady=0)
        
        RightFrame1 = Frame(TopFrame2, bd=5, width=600, height=500, padx=2, bg="GRAY", relief=GROOVE)
        RightFrame1.pack(side=RIGHT)

        
        
        #=============================================TITLE===========================================#
        
        self.lblTitle = Label(TitleFrame, font=('Quicksand',38,'bold'), text="MSU-IIT STUDENT INFORMATION SYSTEM", bg="LIGHTSLATEGRAY",bd=7)
        self.lblTitle.grid(row=0, column=0, padx=190)
        
        #===========================================================================LABELS & ENTRy WIDGETS=======================================================#
        
        self.lblStudentID = Label(LeftFrame1, font=('Quicksand',12,'bold'), text="STUDENT ID:",bg="DARKSLATEGRAY",fg="white", bd=5 , anchor=NW)
        self.lblStudentID.grid(row=0, column=0, sticky=W, padx=3)
        self.txtStudentID = Entry(LeftFrame1, font=('Quicksand',12,'bold'), width=20, justify='left', textvariable = Student_IDNumber)
        self.txtStudentID.grid(row=0, column=1)

        self.lblStudentID = Label(BotFrame1, font=('Quicksand',12,'bold'), text="STUDENT ID:",bg="DARKSLATEGRAY",fg="white", bd=5 , anchor=NW)
        self.lblStudentID.grid(row=4, column=3, sticky=W, padx=3)
        self.txtStudentID = Entry(LeftFrame1, font=('Quicksand',12,'bold'), width=20, justify='left', textvariable = Student_IDNumber)
        self.txtStudentID.grid(row=1, column=1)
        
        
        self.lblLastName = Label(LeftFrame1, font=('Quicksand',12,'bold'), text="LAST NAME:",bg="DARKSLATEGRAY",fg="white",bd=7, anchor=NW)
        self.lblLastName.grid(row=1, column=0, sticky=NW, padx=3)
        self.txtLastName = Entry(LeftFrame1, font=('Quicksand',12,'bold'), width=20, justify='left', textvariable = Student_Last_Name)
        self.txtLastName.grid(row=1, column=1)
        
        self.lblFirstName = Label(LeftFrame1, font=('Quicksand',12,'bold'), text="FIRST NAME:",bg="DARKSLATEGRAY",fg="white", bd=7, anchor=NW)
        self.lblFirstName.grid(row=2, column=0, sticky=NW, padx=3)
        self.txtFirstName = Entry(LeftFrame1, font=('Quicksand',12,'bold'), width=20, justify='left', textvariable = Student_First_Name)
        self.txtFirstName.grid(row=2, column=1)
        
        self.lblMiddleInitial = Label(LeftFrame1, font=('Quicksand',12,'bold'), text="MIDDLE INITIAL:", bg="DARKSLATEGRAY",fg="white",bd=7, anchor=NW)
        self.lblMiddleInitial.grid(row=3, column=0, sticky=NW, padx=3)
        self.txtMiddleInitial = Entry(LeftFrame1, font=('Quicksand',12,'bold'), width=20, justify='left', textvariable = Student_Middle_Initial)
        self.txtMiddleInitial.grid(row=3, column=1)
        
        self.lblCourse = Label(LeftFrame1, font=('Quicksand',12,'bold'), text="COURSE:",bg="DARKSLATEGRAY",fg="white", bd=7, anchor=NW)
        self.lblCourse.grid(row=4, column=0, sticky=NW, padx=3)
        self.txtCourse = Entry(LeftFrame1, font=('Quicksand',12,'bold'), width=20, justify='left', textvariable = Student_Course)
        self.txtCourse.grid(row=4, column=1)
        
        self.lblGender = Label(LeftFrame1, font=('Quicksand',12,'bold'), text="GENDER:", bg="DARKSLATEGRAY",fg="white",bd=7, anchor=NW)
        self.lblGender.grid(row=5, column=0, sticky=NW, padx=3)
        
        self.cboGender = ttk.Combobox(LeftFrame1, font=('Quicksand',12,'bold'), state='readonly', width=18, textvariable = Student_Gender)
        self.cboGender['values'] = ('Female', 'Male')
        self.cboGender.grid(row=5, column=1)
        
        self.lblYearLevel = Label(LeftFrame1, font=('Quicksand',12,'bold'), text="YEAR LEVEL:", bg="DARKSLATEGRAY",fg="white",bd=7, anchor=NW)
        self.lblYearLevel.grid(row=6, column=0, sticky=NW, padx=3)
        
        self.cboYearLevel = ttk.Combobox(LeftFrame1, font=('Quicksand',12,'bold'), state='readonly', width=18, textvariable = Student_YearLevel)
        self.cboYearLevel['values'] = ('1', '2', '3', '4')
        self.cboYearLevel.grid(row=6, column=1)
        
        self.searchbar = Entry(self.root, font=('Quicksand',15,'bold'), textvariable = searchbar, width = 15 )
        self.searchbar.place(x=790,y=95)
        
        
        
        #=========================================================BUTTONS================================================#
        
        self.btnAddNew=Button(self.root, pady=1,bd=4,font=('arial',16,'bold'), padx=10, width=9, height=1,fg="GRAY",bg="BLACK", text='ADD', command=addStudent)
        self.btnAddNew.place(x=20,y=128)
        
        self.btnClear=Button(self.root, pady=1,bd=4,font=('arial',16,'bold'), padx=4, width=10, height=1,fg="GRAY",bg="BLACK", text='CLEAR', command=Clear)
        self.btnClear.place(x=20,y=188)
        
        self.btnUpdate=Button(self.root, pady=1,bd=4,font=('arial',16,'bold'), padx=4, width=10, height=1,fg="GRAY",bg="BLACK", text='UPDATE', command=updateData)
        self.btnUpdate.place(x=20,y=248)

        self.btnEdit=Button(self.root, pady=1,bd=4,font=('arial',16,'bold'), padx=4, width=10, height=1,fg="GRAY",bg="BLACK", text='EDIT', command = editData)
        self.btnEdit.place(x=20,y=368)

        self.btnDisplay=Button(self.root, pady=1,bd=4, font=('arial', 16, 'bold'),padx=4,width=10,height=1, fg="GRAY",bg="BLACK",text="DISPLAY" , command=displayData)
        self.btnDisplay.place(x=20,y=425)


        self.btnDelete=Button(self.root, pady=1,bd=4,font=('arial',16,'bold'), padx=4, width=10, height=1,fg="GRAY",bg="BLACK", text='DELETE',command = deleteData)
        self.btnDelete.place(x=20,y=308)

        self.btnExit=Button(self.root, pady=1,bd=4,font=('arial',16,'bold'), padx=3, width=10,height=1,fg="DARKSLATEGRAY", text='EXIT',bg="BLACK",command = iExit)
        self.btnExit.place(x=1100,y=500)

        self.btnSearch=Button(self.root, pady=1,bd=2,font=('arial',11,'bold'), padx=2, width=13,height=1,text='SEARCH',bg="GRAY", command = searchData)
        self.btnSearch.place(x=950,y=93)

        
        
        #==============================================================================TREEVIEW=========================================================================#
        
        scroll_y=Scrollbar(RightFrame1, orient=VERTICAL)
        
        tree = ttk.Treeview(RightFrame1, height=15, columns=("Student ID Number", "Last Name", "First Name", "Middle Initial", "Gender", "Year Level", "Course"), yscrollcommand=scroll_y.set)
     
        
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=tree.yview)

        tree.heading("Student ID Number", text="Student ID Number")
        tree.heading("Last Name", text="Last Name")
        tree.heading("First Name", text="First Name")
        tree.heading("Middle Initial", text="Middle Initial")
        tree.heading("Gender", text="Gender")
        tree.heading("Year Level", text="Year Level")
        tree.heading("Course", text="Course")
        tree['show'] = 'headings'

        tree.column("Student ID Number", width=120)
        tree.column("Last Name", width=100)
        tree.column("First Name", width=100)
        tree.column("Middle Initial", width=100)
        tree.column("Gender", width=70)
        tree.column("Year Level", width=70)
        tree.column("Course", width=80)
        tree.pack(fill=BOTH,expand=1)
        
       
        
        displayData()
        #===========================================================================================================================================================#
    def saveData(self):
        temps = []
        with open('Studentinfo.csv', "w", newline ='') as update:
            fieldnames = ["Student ID Number","Last Name","First Name","Middle Initial","Gender","Year Level","Course"]
            writer = csv.DictWriter(update, fieldnames=fieldnames, lineterminator='\n')
            writer.writeheader()
            for id, val in self.data.items():
                temp ={"Student ID Number": id}
                for key, value in val.items():
                    temp[key] = value
                temps.append(temp)
            writer.writerows(temps)
            

if __name__ =='__main__':
    root = Tk()
    application = Student(root)
    root.mainloop()
