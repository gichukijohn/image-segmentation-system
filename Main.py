from logging import exception
from tkinter import * 
from tkinter import ttk
import tkinter as tk
from PIL import Image,ImageTk
import os
from mysql.connector import cursor
import segment
from PIL import Image,ImageTk #python3-pil.imagetk python3-imaging-tk
from tkinter import messagebox
import mysql.connector

master=Tk()
master.title("Image Segmentation System")
master.geometry("1350x750+0+0")
master.configure(background='Cadet Blue')
#declare the global variables    
global a1
global b1
global c1
global d1
global e1

#designing the title of the project
load=Image.open("heading1.jpg")
photo=ImageTk.PhotoImage(load)
header=tk.Button(master,image=photo).place(x=5,y=0)    
#designing the GUI of the system by dividing it into partitions using frames
RegistrationFrame=Frame(master,bg='grey',bd=20,pady=5,relief=RIDGE)
RegistrationFrame.place(x=5,y=90,width=1360,height=320)
    
SegmentationFrame=Frame(RegistrationFrame,bg='cyan',bd=20,pady=5,relief=RIDGE)
SegmentationFrame.place(x=930,y=0,width=400,height=275)

SearchFrame=Frame(master,bg='sea green',bd=20,pady=5,relief=RIDGE)
SearchFrame.place(x=5,y=400,width=1360,height=300)

lblRegistration=Label(RegistrationFrame,font=('Algerian',12,'bold'),text="Registration Form",bd=5,fg='black',justify=CENTER)
lblRegistration.grid(row=0,column=0)

lblSearch=Label(SearchFrame,font=('Algerian',12,'bold'),text="List of Patients",fg='black',justify=CENTER)
lblSearch.grid(row=0,column=0)


#a function to perform insertion of a record into the database    
def add():
        PId=a1.get()
        PFirstName=b1.get(); 
        PLastName=c1.get();
        PCity=d1.get();
        PContactNumber=e1.get();
        PAddress=f1.get();
        
        
        if (PId =="" or PFirstName=="" or PLastName=="" or PCity=="" or PContactNumber=="" or PAddress==""):
          messagebox.showerror("Error","enter all information")
        
        else:
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="hospital")
            mycursor=mysqldb.cursor()
            sql="INSERT INTO patient (ID,FirstName,LastName, City,ContactNumber,Address) VALUES(%s,%s,%s,%s,%s,%s)"
            val=(PId,PFirstName,PLastName,PCity,PContactNumber,PAddress)
            mycursor.execute(sql,val)
            mysqldb.commit()
            lastid=mycursor.lastrowid
            messagebox.showinfo("information","record added successfully")
            show()
            a1.delete(0,END)
            b1.delete(0,END)
            c1.delete(0,END)
            d1.delete(0,END)
            e1.delete(0,END) 
            f1.delete(0,END)                    
            a1.focus_set()
            
           
           
#a function to get values of the list into their respective textboxes for editing           
def GetValue(event):
        a1.delete(0,END)
        b1.delete(0,END)
        c1.delete(0,END)
        d1.delete(0,END)
        e1.delete(0,END)
        f1.delete(0,END)
        
        row_id=Listbox.selection()[0]
        select=Listbox.set(row_id)
        a1.insert(0,select['ID'])
        b1.insert(0,select['FirstName'])
        c1.insert(0,select['LastName'])
        d1.insert(0,select['City'])
        e1.insert(0,select['ContactNumber'])
        f1.insert(0,select['Address'])
# a function to update an existing record    
def update():
        PId=a1.get()
        PFirstName=b1.get(); 
        PLastName=c1.get();
        PCity=d1.get();
        PContactNumber=e1.get();
        PAddress=f1.get();
        
        if (PId =="" or PFirstName=="" or PLastName=="" or PCity=="" or PContactNumber=="" or PAddress==""):
          messagebox.showerror("Error","enter all information")    
              
        
        
        else:
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="hospital")
            mycursor=mysqldb.cursor()
            sql="Update patient set FirstName=%s,LastName=%s,City=%s,ContactNumber=%s,Address=%s where ID=%s"
            val=(PFirstName,PLastName,PCity,PContactNumber,PAddress,PId)
            mycursor.execute(sql,val)
            mysqldb.commit()
            lastid=mycursor.lastrowid
            messagebox.showinfo("information","record updated successfully")
            a1.delete(0,END)
            b1.delete(0,END)
            c1.delete(0,END)
            d1.delete(0,END)
            e1.delete(0,END)
            f1.delete(0,END)
            a1.focus_set()
            show()
            
        
 # a function to remove unwanted record from the database     
def Delete():
        PId=a1.get()
               
               
        if (PId =="" ):
          messagebox.showerror("Error","enter ID to delete")   
               
        
        else:
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="hospital")
            mycursor=mysqldb.cursor()
            sql="delete from patient where ID=%s"
            val=(PId,)
            mycursor.execute(sql,val)
            mysqldb.commit()
            lastid=mycursor.lastrowid
            messagebox.showinfo("information","record deleted successfully")
            show()
            a1.delete(0,END)
            b1.delete(0,END)
            c1.delete(0,END)
            d1.delete(0,END)
            e1.delete(0,END)
            f1.delete(0,END)
            a1.focus_set()            
        
#a function to display records in a view list from the database       
def show():
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="hospital")
            mycursor=mysqldb.cursor()
            mycursor.execute("select ID,FirstName,LastName,City,ContactNumber,Address,TestResults FROM patient")
            patients=mycursor.fetchall()
            Listbox.delete(*Listbox.get_children())
            
            print(patients)
            
            for i,(ID,FirstName,LastName,City,ContactNumber,Address,TestResults) in enumerate(patients):
             Listbox.insert("","end", values=(ID,FirstName,LastName,City,ContactNumber,Address,TestResults))                
            mysqldb.close 
#==========================Labels=============================================================================           
a = Label(RegistrationFrame ,width=15,font=('Algerian',12,'bold'),text = "ID",bd=6).place(x=5,y=60)   
b = Label(RegistrationFrame ,width=15,font=('Algerian ',12,'bold'),text = "First Name",bd=6).place(x=5,y=120) 
c = Label(RegistrationFrame ,width=15,font=('Algerian',12,'bold'),text = "Last Name",bd=6).place(x=5,y=180) 
d = Label(RegistrationFrame ,width=15,font=('Algerian',12,'bold'),text = "City",bd=6).place(x=480,y=60) 
e = Label(RegistrationFrame ,width=15,font=('Algerian',12,'bold'),text = "Contact Number",bd=6).place(x=480,y=120) 
f = Label(RegistrationFrame ,width=15,font=('Algerian',12,'bold'),text = "Address",bd=6).place(x=480,y=180) 

#==========================Testboxes===============================================================================
a1 = Entry(RegistrationFrame,width=32,bd=10,font=('arial',10,'bold'))
a1.place(x=200,y=60)
b1 = Entry(RegistrationFrame,width=32,bd=10,font=('arial',10,'bold'))
b1.place(x=200,y=120)
c1 = Entry(RegistrationFrame,width=32,bd=10,font=('arial',10,'bold'))
c1.place(x=200,y=180)
d1 = Entry(RegistrationFrame,width=32,bd=10,font=('arial',10,'bold'))
d1.place(x=675,y=60)
e1 = Entry(RegistrationFrame,width=32,bd=10,font=('arial',10,'bold'))
e1.place(x=675,y=120)
f1 = Entry(RegistrationFrame,width=32,bd=10,font=('arial',10,'bold'))
f1.place(x=675,y=180)  
#===============================Buttons==========================================================
btn1 = Button(RegistrationFrame,text="Save",bd=5,bg='green',width=15,command=add).place(x=5,y=230)
btn2 = Button(RegistrationFrame,text="Delete",bd=5,bg='red',width=15,command=Delete).place(x=150,y=230)
btn3 = Button(RegistrationFrame,text="Update",bd=5,bg='green',width=15,command=update).place(x=300,y=230)

#=============================list==========================================================================


btn1 = Button(SearchFrame,text="Refresh",bd=10,bg='grey',width=15,command=show,font=('Algerian',12,'bold')).grid(row = 1,column = 0,padx=(5, 0))
    
cols=('ID','FirstName','LastName','City','ContactNumber','Address','TestResults')
Listbox=ttk.Treeview(SearchFrame,columns=cols,show='headings')
    
for col in cols:
        Listbox.heading(col,text=col)
        Listbox.grid(row=2,column=0,columnspan=4)
        Listbox.place(x=5,y=80,height=170)
        
show()
Listbox.bind('<Double-Button-1>',GetValue)
    
        


    #================================Segmentation buttons=======================================================================
btn2 = Button(SegmentationFrame,font=('Algerian',12,'bold'),text=">>>Input Image",width=25,bd=10,bg='grey',
command=lambda:segment.openNewWindow(master)).place(x=5,y=30)
btn2 = Button(SegmentationFrame,font=('Algerian',12,'bold'),text="Exit",width=25,bd=10,bg='red',command=master.destroy).place(x=5,y=120)

master.mainloop()