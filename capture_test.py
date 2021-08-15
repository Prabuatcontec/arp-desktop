from numpy.lib import math
from config import Config
from timeit import default_timer as timer
from tkinter.constants import HORIZONTAL
import pytesseract
import cv2
import numpy as np
import structlog
from pyzbar import pyzbar
from modelunitvalidation import ModelValidation

from datetime import datetime 
from filehandling import HoldStatus
import calendar
import random
import time
import re
import json
import threading
from image import ImageProcess
import tkinter as tk
import imutils
from PIL import Image
from PIL import ImageTk
from imutils.video import VideoStream
from mysql import Connection
from tkinter.ttk import Progressbar
import requests
import os
import tkinter.messagebox



logger = structlog.get_logger(__name__)



class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        frame_but_right = tk.Frame(self, width=240, height=60)
        frame_but_right.grid(row=1, column=0, padx=1, pady=1, sticky='nsew')
       
        
        b_ebdata = tk.Button(frame_but_right, text="Login", width=10, height=2, command=lambda: controller.show_frame(PageTwo))
        b_ebdata.grid(row=0, column=0)
        
        # frame_eb_data = tk.Frame(self, width=1200, height=10)
        # frame_eb_data.grid(row=0, column=2, sticky='nsew', padx=1, pady=1)
        #self.progress = Progressbar(frame_eb_data, orient=HORIZONTAL,length=100,  mode='indeterminate')
      
    



class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        frame_eb_data = tk.Frame(self, width=100, height=10)
        frame_eb_data.grid(row=0, column=1, sticky='nsew', padx=1, pady=1)
        lab_eb_data = tk.Label(frame_eb_data, background='#DDD4EF', textvariable=controller.page1_label)
        lab_eb_data.grid(row=0, column=1)
        frame_but_right = tk.Frame(self, width=240, height=60)
        frame_but_right.grid(row=3, column=1, padx=1, pady=1, sticky='nsew')
        b_ebdata = tk.Button(frame_but_right, text="Logout", width=10, height=2, command=lambda: controller.show_frame(PageOne))
        b_ebdata.grid(row=2, column=1)
        self.category = tk.StringVar()
        somechoices = []
        for value in Connection().getCustomer():
           somechoices.append(value[2])

        #somechoices = ["1", "2", "C", "D"]
        self.category.set("Pick a Customer")
        open("static/uploads/_customer.txt", "w").write("")
        open("static/uploads/_model.txt", "w").write("")
        open("static/uploads/_serial.txt", "w").write("")
        open("static/uploads/_goodDataAvailable.txt", "w").write("")
        self.validation = open("static/uploads/_validation.txt", 'r').read()
        self.customer = open("static/uploads/_customer.txt").readline().strip("\n")


        popupMenu = tk.OptionMenu(frame_eb_data, self.category, *somechoices)
        popupMenu.grid(row=1, column=1)

        self.category.trace('w', self.change_dropdown)
        self.model = tk.StringVar()
       

        somechoices = ["TC4400", "PH3004", "VIP250", "DMS2004", "NVG589"]
        
        
        frame_but_right1 = tk.Frame(self, width=240, height=60)
        frame_but_right1.grid(row=2, column=1, padx=1, pady=1, sticky='nsew')
        # popupMenu1 = tk.OptionMenu(frame_but_right1, self.model, *somechoices)
        # self.model.set("Pick a Model")
        # popupMenu1.grid(row=1, column=2)
        self.model.trace('w', self.option_select)
        self.progress = Progressbar(frame_eb_data, orient=HORIZONTAL,length=100,  mode='indeterminate')

    def option_select(self, *args):
        print (self.model.get())
        open("static/uploads/_model.txt", "w").write(f"{self.model.get()}")

    def change_dropdown(self,*args):
        print( self.category.get() )
        HoldStatus("").writeFile("", "_lastScan")
        HoldStatus("").writeFile("2", "_scan")
        HoldStatus("").writeFile("0", "_serialpostCount")
        HoldStatus("").writeFile("", "_goodData")
        HoldStatus("").writeFile("0", "_processing")
        open("static/uploads/_serial.txt", "w").write("")
        open("static/uploads/_status.txt", "w").write("")
        dict = {}
        self.progress.grid(row=2,column=0)
        self.progress.start()
        # menu = self.model["menu"]
        # menu.delete(0, "end")
        for value in Connection().getModels(self.category.get()):
           mdict1 = {value[1]:value[2]}
           dict.update(mdict1)
        #    menu.add_command(label=value[1], 
        #                      command=lambda value=value[1]: self.om_variable.set(value[1]))
        self.progress.stop()
        self.progress.grid_forget()
        HoldStatus("").writeFile(json.dumps(dict),"_validation")
        
        threading.Thread(target=self.maintenance, daemon=True).start()
        threading.Thread(target=self.postingData, daemon=True).start()
        open("static/uploads/_customer.txt", "w").write(f"{self.category.get() }")
        
      

    def maintenance(self):
        """ Background thread doing various maintenance tasks """
        readText = ImageProcess()
        while True:
            l=threading.Lock()
            l.acquire()
            readText.readData()
            l.release()
            
            

    def postingData(self):
        """ Background thread doing various maintenance tasks """
        readText = ImageProcess()
        while True:
            # do things...
            time.sleep(1)
            readText.postToDeepblu()

        


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Added the self.controller so the method below can use it.
        self.controller = controller
        
        frame_up_left = tk.Frame(self, width=200, height=50,   colormap="new")
        frame_up_left.grid(row=0, column=0, sticky='w', padx=1, pady=1)
        frame_up_left1 = tk.Frame(self, width=200, height=50,   colormap="new")
        frame_up_left1.grid(row=1, column=0, sticky='w', padx=1, pady=1)
        frame_buttons = tk.Frame(self, width=200, colormap="new")
        frame_buttons.grid(row=2, column=0, padx=1, pady=1, sticky='w')

        
        b5 = tk.Button(frame_buttons, text='Login', command= self.update_p2_label)
        b5.grid(row=0, column=0, padx=1, pady=1, sticky='w')
        b6 = tk.Button(frame_buttons, text='Back', command=lambda: controller.show_frame(PageOne))
        b6.grid(row=0, column=1, padx=1, pady=1, sticky='w')

        self.entry_nombre_fld = tk.Entry(frame_up_left, width=25)
        self.entry_nombre_fld.grid(row=0, column=1, sticky='w')
        self.entry_nombre_fld1 = tk.Entry(frame_up_left1, width=25,  show='*')
        self.entry_nombre_fld1.grid(row=0, column=1, sticky='w')
        label_2 = tk.Label(frame_up_left, text="Username:", font=("bold", 14))
        label_2.grid(row=0, column=0, sticky='w')
        label_21 = tk.Label(frame_up_left1, text="Password: ", font=("bold", 14))
        label_21.grid(row=0, column=0, sticky='w')
        lab_eb_data = tk.Label(frame_buttons, textvariable=self.controller.page2_label)
        lab_eb_data.grid(row=3, column=0, columnspan=2)

       
        
        frame_video = tk.Frame(self, width=1400, height=1800, colormap="new")
        frame_video.grid(row=3, column=0, padx=1, pady=1, sticky='e')
        self.validation = self.validation = open("static/uploads/_validation.txt", 'r').read()
        self.customer = open("static/uploads/_customer.txt").readline().strip("\n")
        self.stopEvent = None
        self.frame = frame_video

        tk.Label(self.frame, text='').pack()

        
        #self.vs = VideoStream(0)
        self.vs  = cv2.VideoCapture(Config.CAMERA_NO)
        self.vs .set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
        self.vs .set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
        self.vs.set(cv2.CAP_PROP_AUTOFOCUS, 0)        
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop1, args=())
        self.thread.start()
        self.panel = None
        self.p = []

        threading.Thread(target=self.maintenance, daemon=True).start()
        threading.Thread(target=self.postingData, daemon=True).start()


    # # Added this function to update the page1_label StringVar.
    def update_p2_label(self):
        response = requests.post(
        Config.API_USER_URL + 'users/login', data=json.dumps({"username": self.entry_nombre_fld.get(), "password": self.entry_nombre_fld1.get(), "Site": "Matamoros"}),
        headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            self.controller.page2_label.set("Authentication Failed!")
        else:
            self.controller.page1_label.set(self.entry_nombre_fld.get().upper())
            open("static/uploads/_login.txt", "w").write(f"{self.entry_nombre_fld.get() }")
            self.controller.page3_label.set("Logout")
            self.controller.show_frame(PageThree)
            
    def rotate_bound(self, image, angle):
        return imutils.rotate(image, -angle) 

    def gradiant(self,p1,p2):
        cal =  (p1[1]-p2[1])/(p2[0]-p1[0])
        return cal
    
    def getAngel(self):
        
        if(len(self.p)>=3):
            p1,p2,p3 =self.p[-3:]
            m1 = self.gradiant(p1,p2)
            m2 = self.gradiant(p1,p3)
            aR = math.atan((m2-m1)/(1+(m2*m1)))
            if math.isnan(aR):
                return 0
            aD = round(math.degrees(aR))
            return aD
        
        return 0
         

    def videoLoop(self):
        stats = []
        start = timer()
        while not self.stopEvent.is_set():
            flag,self.frame = self.vs.read()
            if flag is None:
                print ("Failed")
            #self.frame = cv2.imread("sddddd.png")
            #self.frame = imutils.resize(self.frame, width=1200, height=1500)
    
            # OpenCV represents images in BGR order; however PIL
            # represents images in RGB order, so we need to swap
            # the channels, then convert to PIL and ImageTk format
            customer = open("static/uploads/_customer.txt").readline().strip("\n")
            status = open("static/uploads/_status.txt").readline().strip("\n")
            
            if(customer != ""):
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                if status == "Success":
                    cv2.putText(image, "Status:"+status, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 100, 0), 8)
                elif status == "":
                    cv2.putText(image, "Status:Waiting", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 150, 0), 8)
                else:
                    cv2.putText(image, "Status:Failed", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 8)
            else:
                image = cv2.imread("static/uploads/customer1.jpg")
                cv2.putText(image, "CONTEC ARP", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 3, 255, 8)

            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
    
            # if the panel is not None, we need to initialize it
            if self.panel is None:
                self.panel = tk.Label(image=image)
                self.panel.image = image
                self.panel.pack(side="left", padx=10, pady=10)
    
            # otherwise, simply update the panel
            else:
                self.panel.configure(image=image)
                self.panel.image = image

                image = self.frame
                #image = cv2.resize(image, (4000, 2160 ), interpolation=cv2.INTER_CUBIC)
                # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                # image = gray

                # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

                # contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                # cnt = contours
                # s = 1
                # for c in cnt:
                #     if(cv2.contourArea(c)  > 100000):
                #         s = s + 1
                s = 2
                if (s > 1):
                    lo = [0, -5, 5]
                    for x in lo:
                        image1 = self.rotate_bound(image, x)
                        barcodes = pyzbar.decode(image1)
                        if len(barcodes) > 2:
                            image = image1
                            break

                        
                    serials = []


                    for barcode in barcodes:
                        barcodeData = barcode.data.decode("utf-8")
                        if(detect_special_characer(barcodeData) == True):
                            serials.append(barcodeData)

                    s = 0
                    gmt = time.gmtime()
                    ts = calendar.timegm(gmt)
                    
                    fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))

                    if len(serials) > 0:
                        lastScan = HoldStatus("").readFile("_lastScan")
                        # if(str(lastScan) == str(json.dumps([ele for ele in reversed(serials)])) and str(lastScan)!=""):
                        #     s = 1
                        
                        if s == 0:
                            #print("Scanned")
                            print(serials)
                            HoldStatus("").writeFile(json.dumps([ele for ele in reversed(serials)]), "_lastScan")
                            serials.append(fillenameImage)
                            cv2.imwrite("static/processingImg/boxER_%s.png" % fillenameImage, image)
                            file1 = open("static/uploads/_serial.txt", "a")
                            file1.write(json.dumps([ele for ele in reversed(serials)])+"\n")
                            file1.close()

    def maintenance(self):
        """ Background thread doing various maintenance tasks """
        readText = ImageProcess()
        while True:
            l=threading.Lock()
            l.acquire()
            readText.readData()
            l.release()
    
    def postingData(self):
        """ Background thread doing various maintenance tasks """
        readText = ImageProcess()
        while True:
            # do things...
            l=threading.Lock()
            l.acquire()
            readText.postToDeepblu()
            l.release()


    def videoLoop1(self):
        stats = []
        start = timer()
        for filename in os.listdir("static/processingImg/v5/v6/"):
            start = time.time()
            print(filename)
            image = cv2.imread("static/processingImg/v5/v6/"+ filename)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)




            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY   + cv2.THRESH_OTSU)[1]
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
            closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

            _, contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnt = contours
            s = 1
            angle = 0
            for c in cnt:
                #print(cv2.contourArea(c))
                if(cv2.contourArea(c)  > 100000):
                    print("connnnnnnnnnnnnnnnnnn")
                    #print(cv2.contourArea(c))
                    # rows,cols = thresh.shape[:2]
                    # [vx,vy,x,y] = cv2.fitLine(c, cv2.DIST_L2,0,0.01,0.01)
                    # lefty = int((-x*vy/vx) + y)
                    # righty = int(((cols-x)*vy/vx)+y)
                    # # cv2.line(image,(cols-1,righty),(0,lefty),(0,255,0),2)
                    # # cv2.line(image,(cols-1,righty),(0,righty),(0,255,0),2)
                    # print("x="+str(cols-1)+",y="+str(righty)+",x1="+str(0)+",y1="+str(lefty))
                    # self.p.append([cols-1,righty])
                    # self.p.append([0,lefty])
                    # self.p.append([0,righty])

                    rect = cv2.minAreaRect(c)
                    box = np.int0(cv2.boxPoints(rect))
                    #cv2.drawContours(image, [box], 0, (36,255,12), 3) 
                    #print(box)
                    [vx,vy,x,y] = box

                    center_coordinates = (x[0] , vy[0])
                    radius = 20
                    
                    # Blue color in BGR
                    color = (255, 0, 0)
                    
                    # Line thickness of 2 px
                    thickness = 2

                    # cv2.line(image,(x[0],x[1]),(y[0],y[1]),(0,255,0),2)
                    # cv2.line(image,(x[0],x[1]),(x[0],vy[0]),(0,255,0),2)
                    # cv2.line(image,(x[0],vy[0]),(y[0],y[1]),(0,255,0),2)

                    # cv2.putText(image, "M1", (x[0],x[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 100, 0), 8)
                    # cv2.putText(image, "M2", (y[0],y[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 100, 0), 8)
                    # cv2.putText(image, "M3", center_coordinates, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 100, 0), 8)
                    # Using cv2.circle() method
                    # Draw a circle with blue line borders of thickness of 2 px
                    # image = cv2.circle(image, (x[0],x[1]), radius, color, thickness)
                    # image = cv2.circle(image, (y[0],y[1]), radius, color, thickness)
                    # image = cv2.circle(image, center_coordinates, radius, color, thickness)

                    self.p.append([x[0],x[1]+1])
                    self.p.append([x[0]-1,vy[0]])
                    self.p.append([y[0],y[1]])
                    x = self.getAngel()
                    print('ang')
                    print(x)

                    min_area = 0.95*180*35
                    max_area = 1.05*180*35
                    area = cv2.contourArea(c)
                    #print(rect)
                    image = self.rotate_bound(thresh, x)
                    barcodes = pyzbar.decode(image)
                    serials = []
                    if (len(barcodes)>0):
                        gmt = time.gmtime()
                        ts = calendar.timegm(gmt)
                        fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
                        cv2.imwrite("static/processingImg/22222222222boxER_%s.png" % fillenameImage, image)
                        angle = x
                        for barcode in barcodes:
                            barcodeData = barcode.data.decode("utf-8")
                            if(detect_special_characer(barcodeData) == True):
                                serials.append(barcodeData)
                        
                        if len(serials)>0:
                            text = pytesseract.image_to_string(Image.fromarray(image),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
                            print("".join(text.split()).encode('utf8'))
                            image1 = self.rotate_bound(image, 90)
                            cv2.imwrite("static/processingImg/9022222222222boxER_%s.png" % fillenameImage, image1)
                            text = pytesseract.image_to_string(Image.fromarray(image1),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
                            print("".join(text.split()).encode('utf8'))
                            image2 = self.rotate_bound(image, -90)
                            cv2.imwrite("static/processingImg/minus9022222222222boxER_%s.png" % fillenameImage, image2)
                            text = pytesseract.image_to_string(Image.fromarray(image2),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
                            print("".join(text.split()).encode('utf8'))

                            
                        print(serials)
                        break
                    #print(barcodes)

                    # serials = []


                    for barcode in barcodes:
                        barcodeData = barcode.data.decode("utf-8")
                        if(detect_special_characer(barcodeData) == True):
                            stats.append(barcodeData)

                    #
                    
                    #condition to skip the light effect 
                    # if vx[0] == 0 and vx[1] == 0 :
                    #     s = 1
                    # else: 
                    #     s = s + 1
                    s = s + 1
                    x,y,w,h = cv2.boundingRect(c)

            if s > 1:
                
                gmt = time.gmtime()
                ts = calendar.timegm(gmt)
                fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
                cv2.imwrite("static/processingImg/22222222222boxER_%s.png" % fillenameImage, image)



                

                cv2.imwrite("static/processingImg/RotateboxER_%s.png" % fillenameImage, image)
        print (stats)
        return 1

            # barcodes = pyzbar.decode(image)
                    
            # serials = []


            # for barcode in barcodes:
            #     barcodeData = barcode.data.decode("utf-8")
            #     if(detect_special_characer(barcodeData) == True):
            #         serials.append(barcodeData)

            # print(serials)
            # s = 0
            
            
            # if len(serials) > 0:
                
            #     if s == 0:
            #         print(serials)
                    
            #         thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            #         _, contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            #         cnt = contours
            #         s = 1
            #         for c in cnt:
            #             #print(cv2.contourArea(c))
            #             if(cv2.contourArea(c)  > 100000):
            #                 # rows,cols = thresh.shape[:2]
            #                 # [vx,vy,x,y] = cv2.fitLine(c, cv2.DIST_L2,0,0.01,0.01)
            #                 # lefty = int((-x*vy/vx) + y)
            #                 # righty = int(((cols-x)*vy/vx)+y)
            #                 # # cv2.line(image,(cols-1,righty),(0,lefty),(0,255,0),2)
            #                 # # cv2.line(image,(cols-1,righty),(0,righty),(0,255,0),2)
            #                 # print("x="+str(cols-1)+",y="+str(righty)+",x1="+str(0)+",y1="+str(lefty))
            #                 # self.p.append([cols-1,righty])
            #                 # self.p.append([0,lefty])
            #                 # self.p.append([0,righty])

            #                 rect = cv2.minAreaRect(c)
            #                 box = np.int0(cv2.boxPoints(rect))
            #                 [vx,vy,x,y] = box

            #                 # center_coordinates = (x[0] , vy[0])
            #                 # radius = 20
                            
            #                 # # Blue color in BGR
            #                 # color = (255, 0, 0)
                            
            #                 # # Line thickness of 2 px
            #                 # thickness = 2
                            
            #                 # # Using cv2.circle() method
            #                 # # Draw a circle with blue line borders of thickness of 2 px
            #                 # image = cv2.circle(image, (x[0],x[1]), radius, color, thickness)
            #                 # image = cv2.circle(image, (y[0],y[1]), radius, color, thickness)
            #                 # image = cv2.circle(image, center_coordinates, radius, color, thickness)

            #                 self.p.append([x[0],x[1]+1])
            #                 self.p.append([x[0]-1,vy[0]])
            #                 self.p.append([y[0],y[1]])
                            
                            
            #                 s = s + 1
            #                 x,y,w,h = cv2.boundingRect(c)

            #         if s > 1:
            #             gmt = time.gmtime()
            #             ts = calendar.timegm(gmt)
            #             fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
            #             #cv2.imwrite("static/processingImg/22222222222boxER_%s.png" % fillenameImage, image)
            #             text = pytesseract.image_to_string(Image.fromarray(image),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
            #             print("".join(text.split()).encode('utf8'))
            #             image = thresh[y:y+h,x:x+w]
            #             start = time.time()
            #             print(start)
            #             print('start')
            #             image = cv2.resize(image, (3000, 3000 ), interpolation=cv2.INTER_CUBIC)
            #             start = time.time()
            #             print(start)
            #             print('end start')
            #             x = self.getAngel()
            #             image = self.rotate_bound(image, x)
            #             image1 = self.rotate_bound(image, 90)
            #             image2 = self.rotate_bound(image, -90)
            #             start = time.time()
            #             print(start)
            #             print('end')
            #             print(x)
            #             cv2.imwrite("static/processingImg/111111111111boxER_%s.png" % fillenameImage, image)
            #             text = pytesseract.image_to_string(Image.fromarray(image),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
            #             print("".join(text.split()).encode('utf8'))
            #             print(90)
            #             cv2.imwrite("static/processingImg/4522222222222boxER_%s.png" % fillenameImage, image1)
            #             text = pytesseract.image_to_string(Image.fromarray(image1),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
            #             print("".join(text.split()).encode('utf8'))
            #             print(-90)
            #             cv2.imwrite("static/processingImg/minus22222222222boxER_%s.png" % fillenameImage, image2)
            #             text = pytesseract.image_to_string(Image.fromarray(image2),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
            #             print("".join(text.split()).encode('utf8'))
            #             #gray = thresh

            #         #line = self.trimValue(serials)
            #             self.processImage(serials, gray, image)
            #         # HoldStatus("").writeFile(json.dumps([ele for ele in reversed(serials)]), "_lastScan")
            #         # serials.append(fillenameImage)
            #         # open("static/serials/%s.txt" %fillenameImage, "w").write(json.dumps([ele for ele in reversed(serials)]))
            #         # cv2.imwrite("static/processingImg/boxER_%s.png" % fillenameImage, image)
            #         # file1 = open("static/uploads/_serial.txt", "a")
            #         # file1.write(json.dumps([ele for ele in reversed(serials)])+"\n")
            #         # file1.close()

    def Reverse(self, lst):
        return [ele for ele in reversed(lst)]
        
    def trimValue(self, line):
        line = line.replace('"', '')
        line = line.replace('[', '')
        line = line.replace(']', '')
        line = line.split(',')
        return line

    def processImage(self, line, image, image1):
        
        r = open("static/uploads/_goodDataAvailable.txt", "r")
        r = str(r.read())
        rev = self.Reverse(line)
        if(r.find(str(line)) !=-1 or r.find(str(rev)) != -1):
            return 1
        else:
            
            #print("=============================================")
            text = pytesseract.image_to_string(Image.fromarray(image),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
            #print("".join(text.split()).encode('utf8'))
            strVal = str(self.validation)
            models = json.loads(strVal)
            angleSame = 0
            r = 0
            for key, value in models.items():
                sub_index = str("".join(text.split())).find(key.replace('"', ""))
                if sub_index >-1:
                    print(90)
                    text = ""
                    self.processValidation(key, value, line, image, image1)
                    angleSame = 1
                    break
            if(angleSame ==0):
                lo = [180]
                for x in lo:
                    print (x)
                    img = self.rotate_bound(image, x)
                    
                    text = pytesseract.image_to_string(Image.fromarray(img),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
                    #print("".join(text.split()).encode('utf8'))
                    
                    for key, value in models.items():
                        sub_index = str("".join(text.split())).find(key.replace('"', ""))
                        if sub_index >-1:
                            text = ""
                            line = self.Reverse(line)
                            self.processValidation(key, value, line, image, image1)
                            r = 1
                            break
                    if r == 1:
                        break
                
                if r == 1:
                    tkinter.messagebox.showinfo("Welcome to GFG.",  "Hi I'm your message")
                    
                

    def processValidation(self, key, value, line, image, image1):
            valid = str(value).replace("'",'"')
            jsonArray =json.loads(str(valid))
            
            valid = ModelValidation().validate(
                jsonArray["data"], line)
            
            if(valid != '0'):
                line = self.Reverse(line)
                valid = ModelValidation().validate(
                    jsonArray["data"], line)

            if valid == '0':
                dict = {}
                p = 0
                for c in range(len(line)):
                    newline = line[c].replace("\n","").replace(" ","")
                    
                    if(c == 0):
                        mdict1 = {"serial": newline}
                        dict.update(mdict1)
                    else:
                        mdict1 = {str("address"+str(c)): newline}
                        dict.update(mdict1)

                if(p == 0):
                    gmt = time.gmtime()
                    ts = calendar.timegm(gmt)
                    
                    fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
                    open("static/uploads/_goodDataAvailable.txt", "a").write(str(line)+"\n")
                    cv2.imwrite("static/processingImg/boxER_%s.png" % fillenameImage, image)
                    start = time.time()
                    print(start)
                    if( str(jsonArray["model"]) == 'DMS2004UHD'):
                        cv2.imwrite("static/processingImg/dms/boxER_%s.png" % fillenameImage, image)
                        cv2.imwrite("static/processingImg/dms/real/boxER_%s.png" % fillenameImage, image1)
                    else:
                        cv2.imwrite("static/processingImg/vip250/boxER_%s.png" % fillenameImage, image)
                        cv2.imwrite("static/processingImg/vip250/real/boxER_%s.png" % fillenameImage, image1)
                    # mdict1 = {"model": str(jsonArray["model"])}
                    # dict.update(mdict1)
                    # mdict1 = {"customer": str(self.customer)}
                    # dict.update(mdict1)
                
                    # open("static/uploads/_status.txt", "w").write("Success")
                    # file1 = open("static/uploads/_goodData.txt", "a")
                    # file1.write("\n")
                    # file1.write(str(dict))
                    # line = str(dict).replace("'",'"')
                    # response = requests.post(Config.DEEPBLU_URL + '/autoreceive/automation', line,
                    #                     headers={'Content-Type': 'application/json', 
                    #                     'Authorization': 'Basic QVVUT1JFQ0VJVkU6YXV0b0AxMjM=' }
                    #                     )
            


class Arp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #self.iconbitmap('@icon1.xbm')
        self.title('ARP')
        
        # Moved StringVar()'s to the main class
        self.page1_label = tk.StringVar()
        self.page2_label = tk.StringVar()
        self.page3_label = tk.StringVar()
        self.page2_entry = tk.StringVar()
        open("static/uploads/_login.txt", "w").write("")
        

        container = tk.Frame(self)
        container.pack(side='top')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (PageOne,PageThree, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.configure(background='lightgrey')
            frame.grid(row=0, column=0, sticky='nswe')
        self.show_frame(PageOne)
    
    
        
        

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
 

def detect_special_characer(pass_string):
    regex= re.compile("'") 
    if(regex.search(pass_string) != None): 
        return False
        
    regex= re.compile('[@_!#$%^&*()<>?/\\\|}{~:[\]]"') 
    if(regex.search(pass_string) == None): 
        res = True
    else: 
        res = False
    return(res)
 
 



if __name__ == "__main__":
    app = Arp()
    app.mainloop()
    # root = tk.Tk()
    # app = App(root)
    MAINTENANCE_INTERVAL = .1

    
    # root.mainloop()
