from tkinter import * 
from PIL import ImageTk,Image
from tkinter import messagebox
from tkinter import filedialog
import numpy as np 
import cv2 
from matplotlib import pyplot as plt
import math
import mysql.connector

def openNewWindow(master):
    newWindow = Toplevel(master)
    newWindow.title("IMAGE SEGMENTATION")
    newWindow.geometry("1350x750+0+0")
    newWindow.configure(background='Cadet Blue')

    #select a an image from file explorer or anywhere you have stored your CT Images
    def file_opener():
       
        input1 =filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("[PNG]","*.png*"),("[JPG]","*.jpg*"),("all files","*.*")))
        aa1.set(input1)
        if not input1:
            messagebox.showerror("Error","you have not selected an image")

    def SEGMENTTEST():
        # Image operation using thresholding 
        img = cv2.imread(aa1.get()) 
        gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        test = ImageTk.PhotoImage(Image.fromarray(gray1))
        label1 = Label(newWindow,image=test)
        label1.image = test
        label1.grid(row = 3,column = 0,columnspan=3)

        #To Get Accuracy Highlight Dark and Light area
        light_val = (150, 150, 150)
        dark_val = (200, 200, 200)
        mask = cv2.inRange(gray1, light_val, dark_val)
        result = cv2.bitwise_and(gray1, gray1, mask=mask)

       

        #To Again Convert Into Gray For threshold
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY) 

       
        
        edges = cv2.Canny(mask,130,300)

        

        # Marker labelling
        ret, markers = cv2.connectedComponents(mask)

        h, w = gray1.shape[:2]
        hue_markers = np.uint8(179*np.float32(markers)/np.max(markers))
        blank_channel = 255*np.ones((h, w), dtype=np.uint8)
        marker_img = cv2.merge([hue_markers, blank_channel, blank_channel])
        marker_img = cv2.cvtColor(marker_img, cv2.COLOR_HSV2BGR)
        
        test = ImageTk.PhotoImage(Image.fromarray(marker_img))
        label2 = Label(newWindow,image=test)
        label2.image = test
        label2.grid(row = 3,column = 2,columnspan=3)

        hsv = cv2.cvtColor(marker_img,cv2.COLOR_BGR2HSV)
        lower_red = np.array([0,120,70])
        upper_red = np.array([10,255,255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        # Range for upper range
        lower_red = np.array([170,120,70])
        upper_red = np.array([180,255,255])
        mask2 = cv2.inRange(hsv,lower_red,upper_red)
        #Generating the final mask to detect red color
        #mask1 = mask1+mask2   
        mask2 = cv2.bitwise_not(mask1)
        res1 = cv2.bitwise_and(marker_img,marker_img,mask=mask2)

        height,width = res1.shape[:2]
        for loop1 in range(height):
            for loop2 in range(width):
                r,g,b = res1[loop1,loop2]
                res1[loop1,loop2] = 0,g,0

        BROWN_MIN = np.array([0, 250, 0], np.uint8)
        BROWN_MAX = np.array([0, 255, 0], np.uint8)
        dst = cv2.inRange(res1, BROWN_MIN, BROWN_MAX)
        no_brown = cv2.countNonZero(dst)
        heartpix=(height*width)/3;
        perval=no_brown/(heartpix/100)
        perval=math.ceil(perval);
        cc1.set(str(perval))
        
        res2 = cv2.bitwise_and(img, img, mask = mask1)
        final_output = cv2.addWeighted(res1,1,res2,1,0)

        test = ImageTk.PhotoImage(Image.fromarray(final_output))
        label3 = Label(newWindow,image=test)
        label3.image = test
        label3.grid(row = 3,column = 4,columnspan=3)
        Mess=""
        if perval>=10:
            Mess="High Risk"
        elif perval>=5 and perval<10:
            Mess="Min Risk"
        elif perval>=1 and perval<5:
            Mess="Low Risk"
        else:
            Mess="No Risk"
        messagebox.showinfo(title="Test Result", message=Mess+", "+str(perval)+"% Infection Detected")
        
    def update():
       
        if(cc1.get()=="" or pid1.get()==""):
          messagebox.showinfo("information","enter all information") 
        
       
        
        else:
            mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="hospital")
            mycursor=mysqldb.cursor()
            sql="update patient SET TestResults='"+cc1.get()+"' where ID='"+pid1.get()+"'"
            
            mycursor.execute(sql)
            mysqldb.commit()
            lastid=mycursor.lastrowid
            messagebox.showinfo("information","record updated successfully")        

    a = Label(newWindow ,width=25,font=('Algerian',12,'bold'),text = "Select Image").grid(row = 1,column = 0,pady=(10, 10),padx=(5, 0))
    aa1 = StringVar()
    a1 = Entry(newWindow,width=30,textvariable=aa1,font=('arial',10,'bold')).grid(row = 1,column = 1,pady=(10, 10))
    btn1 = Button(newWindow,text=">>SelectFile",bd=10,bg='grey',width=20,font=('arial',12,'bold'),command=lambda:file_opener()).grid(row = 1,column = 2,padx=(5, 0))
    btn2 = Button(newWindow,text="Segment",bd=10,bg='light green',width=20,command=SEGMENTTEST).grid(row = 1,column = 3,padx=(5, 0))
    btn3 = Button(newWindow,text="Exit",width=20,bd=10,bg='red',command=newWindow.destroy).grid(row = 1,column = 4,padx=(5, 0))

    cc1 = StringVar()
    cc1.set("0")
    b = Label(newWindow ,width=25,font=('Algerian',12,'bold'),text = "Results(%)").grid(row = 2,column = 0,pady=(10, 10),padx=(5, 0))
    c = Entry(newWindow ,width=25,textvariable=cc1,font=('arial',10,'bold')).grid(row = 2,column = 1,pady=(10, 10),padx=(5, 0))
    
    
            
    u = Label(newWindow ,width=25,font=('Algerian',12,'bold'),text = "Enter User ID").grid(row = 2,column = 2,pady=(10, 10),padx=(5, 0))
    pid1 = StringVar()
    pid = Entry(newWindow,width=30,textvariable=pid1).grid(row = 2,column = 3,pady=(10, 10))
    btnu1 = Button(newWindow,text="Update",width=20,bd=10,bg='light green',command=update).grid(row = 2,column = 4,padx=(5, 0))
