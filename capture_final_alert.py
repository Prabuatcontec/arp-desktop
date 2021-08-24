from config import Config
from timeit import default_timer as timer
from tkinter.constants import HORIZONTAL
import pytesseract
from numpy.lib import math
import cv2
import numpy as np
import structlog
from pyzbar import pyzbar
import pickle

from datetime import datetime 
from filehandling import HoldStatus
import calendar
import random
import time
import re
import os
import sys
import json
import threading
from image import ImageProcess
from conveyor import Conveyor
import tkinter as tk
import imutils
from PIL import Image
from PIL import ImageTk
from imutils.video import VideoStream
from mysql import Connection
from tkinter.ttk import Progressbar
import requests
from modelunitvalidation import ModelValidation
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
        global on, frame, lbx
        frame_eb_data = tk.Frame(self, width=100, height=10)
        frame_eb_data.grid(row=0, column=1, sticky='nsew', padx=1, pady=1)
        lab_eb_data = tk.Label(frame_eb_data, background='#DDD4EF', textvariable=controller.page1_label)
        lab_eb_data.grid(row=0, column=1)

        frame_but_one = tk.Frame(self, width=240, height=60)
        frame_but_one.grid(row=0, column=2, padx=1, pady=1, sticky='nsew')

        b5 = tk.Button(frame_but_one, bg='#A877BA', text='Restart', command=self.removeStatus)
        b5.grid(row=0, column=2, padx=1, pady=1, sticky='w')
        # b6 = tk.Button(frame_but_one, text='Stop', command=self.closeConv)
        # b6.grid(row=0, column=1, padx=1, pady=1, sticky='w')


        frame_but_right = tk.Frame(self, width=240, height=60)
        frame_but_right.grid(row=3, column=1, padx=1, pady=1, sticky='nsew')
        b_ebdata = tk.Button(frame_but_right, text="Logout", width=10, height=2, command=lambda: controller.show_frame(PageOne))
        b_ebdata.grid(row=3, column=1)

        self.model = tk.StringVar()
        frame = tk.Frame(self, width=240, height=60)
        frame.grid(row=1, column=1, padx=1, pady=1, sticky='nsew')

        frame._grid_info = frame.grid_info()
        frame.grid_remove()
        somechoices = ["F", "C", "T"]
        popupMenu1 = tk.OptionMenu(frame, self.model, *somechoices)
        self.model.set("Return Type")
        popupMenu1.grid(row=1, column=2)
        self.model.trace('w', self.option_select)

        self.category = tk.StringVar()
        somechoices = []
        for value in Connection().getCustomer():
           somechoices.append(value[2])

        

        #somechoices = ["1", "2", "C", "D"]
        self.category.set("Pick a Customer")
        open(get_correct_path("static/uploads/_customer.txt"), "w").write("")
        open(get_correct_path("static/uploads/_model.txt"), "w").write("")
        open(get_correct_path("static/uploads/_rtype.txt"), "w").write("")
        #open("static/uploads/_serial.txt", "w").write("")
        open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("0")

        popupMenu = tk.OptionMenu(frame_eb_data, self.category, *somechoices)
        popupMenu.grid(row=1, column=0)

        self.category.trace('w', self.change_dropdown)
       
       

        
        
        
        
        self.progress = Progressbar(frame_eb_data, orient=HORIZONTAL,length=100,  mode='indeterminate')

    def grid_hide(self, widget):
        widget._grid_info = widget.grid_info()
        widget.grid_remove()

    def grid_show(self, widget):
        widget.grid(**widget._grid_info)


    def option_select(self, *args):
        print (self.model.get())
        open(get_correct_path("static/uploads/_rtype.txt"), "w").write(f"{self.model.get()}")

    def callConv(self):
        Conveyor().callAllConveyor()

    def removeStatus(self):
        open(get_correct_path("static/uploads/_status.txt"), "w").write("")
        open(get_correct_path("static/uploads/_lastFail.txt"), "w").write("")
        open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("0")
        Conveyor().enableLight("OFF")

    def closeConv(self):
        Conveyor().CloseAllConveyor()

    
    

    

    def change_dropdown(self,*args):
        open(get_correct_path("static/uploads/_customer.txt"), "w").write(f"{self.category.get() }")
        open(get_correct_path("static/uploads/_status.txt"), "w").write("")
        open(get_correct_path("static/uploads/_lastFail.txt"), "w").write("")
        open(get_correct_path("static/uploads/_rtype.txt"), "w").write("")
        Conveyor.resetLastScan("", "")
        open(get_correct_path("static/uploads/_goodDataAvailable.txt"), "w").write("")
        open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("")
        open(get_correct_path("static/uploads/_serialC.txt"), "w").write("0")

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
        open(get_correct_path("static/uploads/_validation.txt"), "w").write(json.dumps(dict))
        if (self.category.get() == "FRONTIERC0"):
            frame.grid(**frame._grid_info)
        else:
            frame._grid_info = frame.grid_info()
            frame.grid_remove()

        
        
        
        
        #threading.Thread(target=self.maintenance, daemon=True).start()
        # threading.Thread(target=self.postingData, daemon=True).start()
        
      

    def maintenance(self):
        """ Background thread doing various maintenance tasks """
        readText = ImageProcess()
        while True:
            l=threading.Lock()
            l.acquire()
            readText.conStatus()
            l.release()
            
            

    def postingData(self):
        """ Background thread doing various maintenance tasks """
        readText = ImageProcess()
        while True:
            lo=threading.Lock()
            lo.acquire()
            readText.postToDeepblu()
            lo.release()

        


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
        
        self.stopEvent = None
        self.frame = frame_video

        tk.Label(self.frame, text='').pack()

        
        #self.vs = VideoStream(0)
        self.vs  = cv2.VideoCapture(Config.CAMERA_NO)
        self.vs .set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
        self.vs .set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
        self.vs.set(cv2.CAP_PROP_AUTOFOCUS, 0)        
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        self.panel = None
        self.p = []
        self.ang = []


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
            open(get_correct_path("static/uploads/_login.txt"), "w").write(f"{self.entry_nombre_fld.get() }")
            self.controller.page3_label.set("Logout")
            self.controller.show_frame(PageThree)
            
    def rotate_bound(self, image, angle):
        # grab the dimensions of the image and then determine the
        # center
        (h, w) = image.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        # grab the rotation matrix (applying the negative of the
        # angle to rotate clockwise), then grab the sine and cosine
        # (i.e., the rotation components of the matrix)
        M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        # compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))
        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY
        # perform the actual rotation and return the image
        return cv2.warpAffine(image, M, (nW, nH))
    
    def videoLoop(self):
        stats = []
        start = timer()
        while not self.stopEvent.is_set():
            flag,self.frame = self.vs.read()
            if flag is None:
                print ("Failed")
            customer = open(get_correct_path("static/uploads/_customer.txt")).readline().strip("\n")
            
            
            if(customer != ""):
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                _status = open(get_correct_path("static/uploads/_status.txt")).readline().strip("\n")
                
                if _status != "":
                    cv2.putText(image, _status, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 8)
            else:
                image = cv2.imread(get_correct_path("static/uploads/customer1.jpg"))
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
                if image is not None:
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    
                    if(customer != ""):
                        s9 = 1
                        
                        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY   + cv2.THRESH_OTSU)[1]
                        contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]
                        cnt = contours
                        s = 1

                        an = []
                        for c in cnt:
                            if(cv2.contourArea(c)  > 100000):
                                an.append(int(cv2.contourArea(c)))
                        an.sort(reverse = True)
                        i = len(an)
                        poi = 0
                        po = 0
                        if len(an)>0:
                            
                            for c in cnt:
                                if(cv2.contourArea(c)  > 100000):
                                    print(cv2.contourArea(c))
                                    i = i - 1
                                    if(int(cv2.contourArea(c))  == an[0]):
                                        #image = cv2.resize(thresh, (3000, 3000 ), interpolation=cv2.INTER_CUBIC)
                                        serialC = open(get_correct_path("static/uploads/_serialC.txt")).readline().strip("\n")
                                        if(serialC=="0"):
                                            time.sleep(1)
                                            open(get_correct_path("static/uploads/_serialC.txt"), "w").write("1")
                                        else:
                                            open(get_correct_path("static/uploads/_serialC.txt"), "w").write("0")

                                            #print(cv2.contourArea(c))
                                            rect = cv2.minAreaRect(c)
                                            box = np.int0(cv2.boxPoints(rect))
                                            [vx,vy,x,y] = box
                                            radius = 20
                            
                                            self.p = []
                                            self.p.append([x[0],x[1]+1])
                                            self.p.append([x[0]-1,vy[0]])
                                            self.p.append([y[0],y[1]])
                                            x,y,w,h = cv2.boundingRect(c)
                                            gmt = time.gmtime()
                                            ts = calendar.timegm(gmt)
                                            fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
                                            #cv2.imwrite(get_correct_path("static/processingImg/1Bfrrot1boxER_%s.png") % fillenameImage, image)
                                            barcodes = pyzbar.decode(image)

                                            serials = []
                                            for barcode in barcodes:
                                                barcodeData = barcode.data.decode("utf-8")
                                                if(detect_special_characer(barcodeData) == True):
                                                    serials.append(barcodeData)

                                            if len(serials)<1:
                                                x = self.getAngel()
                                                print(x)
                                                print(serials)

                                                image = self.rotate_bound(image, x)
                                                barcodes = pyzbar.decode(image)
                                                
                                                #cv2.imwrite(get_correct_path("static/processingImg/Bfrrot1boxER_%s.png") % fillenameImage, image)
                                                serials = []
                                                for barcode in barcodes:
                                                    barcodeData = barcode.data.decode("utf-8")
                                                    if(detect_special_characer(barcodeData) == True):
                                                        serials.append(barcodeData)

                                                if (len(serials)>0):
                                                    s9 = s9 + 1
                                                    poi = i
                                                    self.ang = [180, 90, -90]
                                                    break
                                            else:
                                                s9 = s9 + 1
                                                poi = i
                                                self.ang = [180, 5, -5, 175, 185]
                                                break
                                    
                                    if (len(an) == i):
                                        break
                                    if po == 1:
                                        break
                        
                        if s9 > 1 :
                            start = time.time()
                            print(start)
                            s = 2
                            if open(get_correct_path("static/uploads/_serialUpdate.txt")).readline().strip("\n") == "1":
                                s = 1
                            if (s > 1):
                                open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("1")
                                gmt = time.gmtime()
                                ts = calendar.timegm(gmt)
                                fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
                                cv2.imwrite(get_correct_path("static/processingImg/111Bfrrot1boxER_%s.png") % fillenameImage, image)
                                r = open(get_correct_path("static/uploads/_goodDataAvailable.txt"), "r")
                                r = str(r.read())
                                rev = self.Reverse(serials)

                                str1 = " " 
                                if str(str1.join(serials)) == open(get_correct_path("static/uploads/_lastFail.txt")).readline().strip("\n"):
                                    serials = []
                                    print(1111)
                                
                                str1 = " " 
                                if str(str1.join(rev)) == open(get_correct_path("static/uploads/_lastFail.txt")).readline().strip("\n"):
                                    serials = []
                                    print(11112)

                                if(r.find(str(serials)) !=-1 or r.find(str(rev)) != -1):
                                    open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("0")
                                else:
                                    if len(serials) > 1:
                                            print(serials)
                                            if s > 1:
                                                thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY   + cv2.THRESH_OTSU)[1]
                                                contourse,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]
                                                cnte = contourse
                                                an1 = []
                                                for c1 in cnte:
                                                    if(cv2.contourArea(c1)  >100000):
                                                        an1.append(int(cv2.contourArea(c1)))
                                                print(an1)
                                                an1.sort(reverse = True)
                                                
                                                for c2 in cnte:
                                                    #print(cv2.contourArea(c))
                                                    if(int(cv2.contourArea(c2))  == an1[0]):
                                                        x,y,w,h = cv2.boundingRect(c2)
                                                        t = image[y:y+h,x:x+w]
                                                        barcodes = pyzbar.decode(t)

                                                        if (len(barcodes)<1):
                                                            t = image

                                                        po = 1
                                                        self.processImage(serials, t, image)
                                                        break
                                            else:
                                                open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("0")

                                    else:
                                        open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("0")
                        else:
                            open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("0")


    def Reverse(self, lst):
        return [ele for ele in reversed(lst)]
        

    def processImage(self, line, image, image1):
        
        r = open(get_correct_path("static/uploads/_goodDataAvailable.txt"), "r")
        r = str(r.read())
        rev = self.Reverse(line)
        if(r.find(str(line)) !=-1 or r.find(str(rev)) != -1):
            open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("0")
            return 1
        else:
                
            validation = open(get_correct_path("static/uploads/_validation.txt"), 'r').read()
            #print("=============================================")
            text = pytesseract.image_to_string(Image.fromarray(image),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
            print("".join(text.split()).encode('utf8'))
            strVal = str(validation)
            models = json.loads(strVal)
            angleSame = 0
            r = 0
            for key, value in models.items():
                calib_result_pickle = pickle.load(open(get_correct_path("static/uploads/lastScan.p"), "rb" ))
                keystored = calib_result_pickle["key"]
                valuestored = calib_result_pickle["value"]
                if keystored != "" and valuestored !="":
                    key = keystored
                    value = valuestored

                sub_index = str("".join(text.split())).find(key.replace('"', ""))
                if sub_index >-1:
                    # print(key)
                    # print(value)
                    print(90)
                    gmt = time.gmtime()
                    ts = calendar.timegm(gmt)
                    fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
                    cv2.imwrite(get_correct_path("static/processingImg/rot1boxER_%s.png") % fillenameImage, image)
                    text = ""
                    self.processValidation(key, value, line, image, image1)
                    Conveyor.resetLastScan(key, value)
                    angleSame = 1
                    r = 1
                    break
            if(angleSame ==0):
                lo = self.ang
                for x in lo:
                    print (x)
                    
                    img = self.rotate_bound(image, x)

                    gmt = time.gmtime()
                    ts = calendar.timegm(gmt)
                    fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
                    cv2.imwrite(get_correct_path("static/processingImg/22222222222boxER_%s.png") % fillenameImage, img)
                    
                    text = pytesseract.image_to_string(Image.fromarray(img),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
                    print("".join(text.split()).encode('utf8'))
                    
                    for key, value in models.items():
                        sub_index = str("".join(text.split())).find(key.replace('"', ""))
                        if sub_index >-1:
                            text = ""
                            line = self.Reverse(line)
                            self.processValidation(key, value, line, image, image1)
                            Conveyor.resetLastScan(key, value)
                            r = 1
                            break
                    if r == 1:
                        break
                
            if r == 0:
                str1 = " " 
                if str(str1.join(line)) != open(get_correct_path("static/uploads/_lastFail.txt")).readline().strip("\n"):
                    open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("1")
                    open(get_correct_path("static/uploads/_lastFail.txt"), "w").write(str(str1.join(line)))
                    Conveyor().closeConveyor()
                    Conveyor().enableLight("RED")
                    open(get_correct_path("static/uploads/_status.txt"), "w").write("Unit OCR Failed : Try to position the box in 0 or 180 degree and click retry")
                    #tkinter.messagebox.askretrycancel("Unit OCR Failed", "For Units:"+ str1.join(line)+". Try to position the box in 0 or 180 degree and click retry. ")
                    #self.enableLight("OFF")

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

    def processValidation(self, key, value, line, image, image1):
            valid = str(value).replace("'",'"')
            jsonArray =json.loads(str(valid))
            
            valid = ModelValidation().validate(
                jsonArray["data"], line)
            
            if(valid != '0'):
                line = self.Reverse(line)
                valid = ModelValidation().validate(
                    jsonArray["data"], line)
            
            if valid !='0':
                str1 = " " 
                if str(str1.join(line)) != open(get_correct_path("static/uploads/_lastFail.txt")).readline().strip("\n"):
                    open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("1")
                    open(get_correct_path("static/uploads/_lastFail.txt"), "w").write(str(str1.join(line)))
                    Conveyor().closeConveyor()
                    Conveyor().enableLight("RED")
                    open(get_correct_path("static/uploads/_status.txt"), "w").write("Unit Validation Failed: Try to position the box in 0 or 180 degree and click retry")
                    
                
                
                return 1

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
                    customer = open(get_correct_path("static/uploads/_customer.txt")).readline().strip("\n")
                    open(get_correct_path("static/uploads/_goodDataAvailable.txt"), "a").write(str(line)+"\n")
                    
                    mdict1 = {"model": str(jsonArray["model"])}
                    dict.update(mdict1)
                    mdict1 = {"customer": str(customer)}
                    dict.update(mdict1)
                    if (str(customer) == "FRONTIERC0"):
                        rtype = open(get_correct_path("static/uploads/_rtype.txt")).readline().strip("\n")
                        if rtype != "":
                            c = c+1
                            mdict1 = {str("address"+str(c)): rtype}
                            dict.update(mdict1)
                    print(dict)
                    line = str(dict).replace("'",'"')
                    requests.post(Config.DEEPBLU_URL + '/autoreceive/automation', line,
                                        headers={'Content-Type': 'application/json', 
                                        'Authorization': 'Basic QVVUT1JFQ0VJVkU6YXV0b0AxMjM=' }
                                        )
                    print('success')
                    Conveyor().enableLight("GREEN")
                    open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("0")
                    open(get_correct_path("static/uploads/_status.txt"), "w").write("")
                    open(get_correct_path("static/uploads/_lastFail.txt"), "w").write("")
                    Conveyor().callConveyor()
                    start = time.time()
                    print(start)



class Arp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('ARP')
        # Moved StringVar()'s to the main class
        self.page1_label = tk.StringVar()
        self.page2_label = tk.StringVar()
        self.page3_label = tk.StringVar()
        self.page2_entry = tk.StringVar()
        open(get_correct_path("static/uploads/_login.txt"), "w").write("")

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

def get_correct_path(relative_path):
    p = os.path.abspath(".").replace('/dist', "")
    return os.path.join(p, relative_path)


if __name__ == "__main__":
    app = Arp()
    app.mainloop()
    MAINTENANCE_INTERVAL = .1

