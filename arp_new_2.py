from config import Config
from timeit import default_timer as timer
from tkinter.constants import HORIZONTAL
import pytesseract
from numpy.lib import math
import cv2
import numpy as np
import structlog
from pyzbar import pyzbar
import calendar
import random
import time
import re
import os
import json
import threading
from image import ImageProcess
from conveyor import Conveyor
from deepblu import Deepblu
import tkinter as tk
from PIL import Image
from PIL import ImageTk
from mysql import Connection
from tkinter.ttk import Progressbar
import requests
from modelunitvalidation import ModelValidation
from tkinter.messagebox import askokcancel, showinfo, WARNING
import socket
from datetime import datetime 

class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        frame_but_right = tk.Frame(self, width=1000, height=2)
        frame_but_right.grid(row=0, column=0, padx=1, pady=1, sticky='nsew')
       
        
        b_ebdata = tk.Button(frame_but_right, text="Login", background='#59981A', width=10, height=2,  command=lambda: controller.show_frame(LoginFrame))
        b_ebdata.grid(row=0, column=0)

        b_ebdata = tk.Button(frame_but_right, text="Close", width=10, height=2, background='#D10000',  command=Close)
        b_ebdata.grid(row=0, column=1)
      
    



class ScanFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        global on, frame, lbx
        frame_eb_data = tk.Frame(self, width=100, height=10)
        frame_eb_data.grid(row=0, column=1, sticky='nsew', padx=1, pady=1)
        lab_eb_data = tk.Label(frame_eb_data, background='#DDD4EF', textvariable=controller.loginName)
        lab_eb_data.grid(row=0, column=1)

        frame_but_one = tk.Frame(self, width=240, height=10)
        frame_but_one.grid(row=4, column=1, padx=1, pady=1, sticky='nsew')

        b5 = tk.Button(frame_but_one, bg='#18A558', text='Restart', height=2, command=self.removeStatus)
        b5.grid(row=0, column=1, padx=1, pady=1, sticky='w')

        entry_nombre_fld1c = tk.Entry(frame_eb_data)
        entry_nombre_fld1c.grid(row=0, column=2, sticky='w')

        entry_nombre_fld1c.config(textvariable=controller.updatePalletId, relief='flat')
        entry_nombre_fld1c.grid(row=0, column=2)


        frame_but_right = tk.Frame(self, width=240, height=10)
        frame_but_right.grid(row=3, column=1, padx=1, pady=1, sticky='nsew')
        b_ebdata = tk.Button(frame_but_right, text="Logout", width=10, height=2, background='#FFA500',  command=lambda: controller.show_frame(HomeFrame))
        b_ebdata.grid(row=3, column=1)
        b_ebdata = tk.Button(frame_but_right, text="Close", width=10, height=2, background='#D10000',  command=Close)
        b_ebdata.grid(row=3, column=0)

        self.model = tk.StringVar()
        frame = tk.Frame(self, width=240, height=10)
        frame.grid(row=1, column=1, padx=1, pady=1, sticky='nsew')

        frame._grid_info = frame.grid_info()
        frame.grid_remove()
        somechoices = ["Field Return", "Customer Return", "Technical Support Return"]
        popupMenu1 = tk.OptionMenu(frame, self.model, *somechoices)
        self.model.set("Customer Return")
        popupMenu1.grid(row=1, column=2)
        self.model.trace('w', self.ReturnTypeSelect)

        self.customerSelect = tk.StringVar()
        somechoices = []
        for value in Connection().getCustomer():
           somechoices.append(value[2])

        
        self.customerSelect.set("Pick a Customer")

        popupMenu = tk.OptionMenu(frame_eb_data, self.customerSelect, *somechoices)
        popupMenu.grid(row=1, column=0)

        self.customerSelect.trace('w', self.chooseCustomer)

        b_ebdata = tk.Button(frame_eb_data, text="Close Pallet", width=10, height=2, background='#D10000',  command=self.ClosePallet)
        b_ebdata.grid(row=1, column=2)

    def grid_hide(self, widget):
        widget._grid_info = widget.grid_info()
        widget.grid_remove()

    def grid_show(self, widget):
        widget.grid(**widget._grid_info)


    def ReturnTypeSelect(self, *args):
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

    def chooseCustomer(self,*args):
        resetScanData()
        open(get_correct_path("static/uploads/_customer.txt"), "w").write(f"{self.customerSelect.get() }")
        

        dict = {}
        for value in Connection().getModels(self.customerSelect.get()):
           mdict1 = {value[1]:value[2]}
           dict.update(mdict1)
        open(get_correct_path("static/uploads/_validation.txt"), "w").write(json.dumps(dict))
        if (self.customerSelect.get() == "FRONTIERC0"):
            frame.grid(**frame._grid_info)
        else:
            frame._grid_info = frame.grid_info()
            frame.grid_remove()

        threading.Thread(target=self.maintenance, daemon=True).start()
        
      

    def maintenance(self):
        """ Background thread doing various maintenance tasks """
        while True:
            l=threading.Lock()
            l.acquire()
            calib_result_pickle = Conveyor.getScan()
            model = calib_result_pickle["model"]
            if model != "":
                response = Deepblu().getPalletId(model)
                if response.status_code != 200:
                    self.controller.loginResult.set("Deepblu Pallet Falied!")
                else:
                    a = response.json()
                    if len(a)>0:
                        self.controller.updatePalletId.set(a[0]['palletId'])
                        open(get_correct_path("static/uploads/_palletId.txt"), "w").write(str(a[0]['palletId']))

            time.sleep(10)
            l.release()

    def ClosePallet(self):
        answer = askokcancel(
            title='Confirmation',
            message='Do you want to close the pallet?',
            icon=WARNING)

        if answer:
            response = Deepblu().closePallet()
            if response.status_code != 200:
                self.controller.loginResult.set("Deepblu Pallet Falied!")
            else:

                palletDetail = response.json()
                Deepblu().printPalletTag(palletDetail)
                Conveyor.resetLastScan("", "", "")
                

        


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        frame_up_left = tk.Frame(self, width=1000, height=10,   colormap="new")
        frame_up_left.grid(row=0, column=0, sticky='w', padx=1, pady=1)
        frame_up_left1 = tk.Frame(self, width=200, height=10,   colormap="new")
        frame_up_left1.grid(row=1, column=0, sticky='w', padx=1, pady=1)
        frame_buttons = tk.Frame(self, width=200, colormap="new")
        frame_buttons.grid(row=2, column=0, padx=1, pady=1, sticky='w')

        
        b5 = tk.Button(frame_buttons, text='Login', width=10, height=2, background='#59981A',  command= self.login)
        b5.grid(row=0, column=0, padx=1, pady=1, sticky='w')
        b6 = tk.Button(frame_buttons, text='Back', width=10, height=2, background='#FFA500',  command=lambda: controller.show_frame(HomeFrame))
        b6.grid(row=0, column=1, padx=1, pady=1, sticky='w')
        
        b_ebdata = tk.Button(frame_buttons, text="Close", width=10, height=2, background='#D10000',  command=Close)
        b_ebdata.grid(row=2,padx=1, pady=3, column=0)

        

        self.entry_nombre_fld = tk.Entry(frame_up_left, width=25)
        self.entry_nombre_fld.grid(row=0, column=1, sticky='w')
        self.entry_nombre_fld1 = tk.Entry(frame_up_left1, width=25,  show='*')
        self.entry_nombre_fld1.grid(row=0, column=1, sticky='w')
        label_2 = tk.Label(frame_up_left, text="Username:", font=("bold", 14))
        label_2.grid(row=0, column=0, sticky='w')
        label_21 = tk.Label(frame_up_left1, text="Password: ", font=("bold", 14))
        label_21.grid(row=0, column=0, sticky='w')
        lab_eb_data = tk.Label(frame_buttons, foreground='#D10000', textvariable=self.controller.loginResult)
        lab_eb_data.grid(row=3, column=0, columnspan=2)

       
        
        frame_video = tk.Frame(self, colormap="new")
        frame_video.grid(row=3, column=0, padx=1, pady=1, sticky='e')
        frame_video1 = tk.Frame(self, colormap="new")
        frame_video1.grid(row=3, column=1, padx=1, pady=1, sticky='e')
        
        self.stopEvent = None
        self.frame = frame_video
        self.frame1 = frame_video1

        l1 = tk.Label(self.frame, text='')
        l1.grid(row=0, column=0, sticky='w')

        l1 = tk.Label(self.frame1, text='')
        l1.grid(row=0, column=0, sticky='w')

        
        #vs = VideoStream(0)
               
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        self.thread = threading.Thread(target=self.videoLoopOne, args=())
        self.thread.start()
        self.panel = None
        self.p = []
        self.ang = []


    # # Added this function to update the loginName StringVar.
    def login(self):
        response = requests.post(
        Config.API_USER_URL + 'users/login', data=json.dumps({"username": self.entry_nombre_fld.get(), "password": self.entry_nombre_fld1.get(), "Site": "Matamoros"}),
        headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            self.controller.loginResult.set("Authentication Failed!")
        else:
            self.controller.loginName.set(self.entry_nombre_fld.get().upper())
            open(get_correct_path("static/uploads/_login.txt"), "w").write(f"{self.entry_nombre_fld.get() }")
            self.controller.logoutButton.set("Logout")
            self.controller.show_frame(ScanFrame)
            
    def rotateBound(self, image, angle):
        (h, w) = image.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY
        return cv2.warpAffine(image, M, (nW, nH))
    
    def videoLoop(self):
        stats = []
        start = timer()
        while not self.stopEvent.is_set():
            flag,self.frame = vs.read()
            if flag is None:
                print ("Failed")
            customer = open(get_correct_path("static/uploads/_customer.txt")).readline().strip("\n")
            
            if(customer != ""):
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                _status = open(get_correct_path("static/uploads/_status.txt")).read()
                y0, dy = 50, 50
                sub_index = _status.find("New")
                if sub_index >-1:
                    colr = (255, 165, 0)
                else:
                    colr = (255, 0, 0)

                if _status != "":
                    for i, line in enumerate(_status.split('\n')):
                        y = y0 + i*dy
                        cv2.putText(image, line.replace('\n', ""), (50, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, colr, 8)
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
                self.ProcessCam(image, customer)
        
    def videoLoopOne(self):
        stats = []
        start = timer()
        while not self.stopEvent.is_set():
            flag,self.frame1 = vs.read()
            if flag is None:
                print ("Failed")
            customer = open(get_correct_path("static/uploads/_customer.txt")).readline().strip("\n")
            
            if(customer != ""):
                image = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2RGB)
                _status = open(get_correct_path("static/uploads/_status.txt")).read()
                y0, dy = 50, 50
                sub_index = _status.find("New")
                if sub_index >-1:
                    colr = (255, 165, 0)
                else:
                    colr = (255, 0, 0)

                if _status != "":
                    for i, line in enumerate(_status.split('\n')):
                        y = y0 + i*dy
                        cv2.putText(image, line.replace('\n', ""), (50, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, colr, 8)
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

                image = self.frame1
                self.ProcessCam(image, customer)
    
    def ProcessCam(self,image, customer):
        if image is not None:
                    if(customer != ""):
                        s9 = 1
                        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY   + cv2.THRESH_OTSU)[1]
                        #image = thresh
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
                                    #print(cv2.contourArea(c))
                                    i = i - 1
                                    if(int(cv2.contourArea(c))  == an[0]):
                                        serialC = open(get_correct_path("static/uploads/_serialC.txt")).readline().strip("\n")
                                        #serialC = "1"
                                        if(serialC=="0"):
                                            time.sleep(2)
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
                                            
                                            barcodes = pyzbar.decode(image)

                                            serials = []
                                            for barcode in barcodes:
                                                barcodeData = barcode.data.decode("utf-8")
                                                if(detect_special_characer(barcodeData) == True):
                                                    serials.append(barcodeData)

                                            if len(serials)<1:
                                                x = self.getAngel()
                                                #print(x)

                                                image = self.rotateBound(image, x)
                                                barcodes = pyzbar.decode(image)
                                                
                                                
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
                                                self.ang = [180]
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
                                
                                str1 = " " 
                                if str(str1.join(rev)) == open(get_correct_path("static/uploads/_lastFail.txt")).readline().strip("\n"):
                                    serials = []

                                if(r.find(str(serials)) !=-1 or r.find(str(rev)) != -1):
                                    open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("0")
                                else:
                                    if len(serials) > 0:
                                            print(serials)
                                            if s > 1:
                                                
                                                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                                                thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY   + cv2.THRESH_OTSU)[1]
                                                contourse,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]
                                                cnte = contourse
                                                an1 = []
                                                for c1 in cnte:
                                                    if(cv2.contourArea(c1)  >100000):
                                                        an1.append(int(cv2.contourArea(c1)))
                                                
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
                                                self.processImage(serials, t, image)
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
            text = pytesseract.image_to_string(Image.fromarray(image),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
            print("".join(text.split()).encode('utf8'))
            strVal = str(validation)
            models = json.loads(strVal)
            angleSame = 0
            r = 0
            for key, value in models.items():
                calib_result_pickle = Conveyor.getScan()
                keystored = calib_result_pickle["key"]
                valuestored = calib_result_pickle["value"]
                if keystored != "" and valuestored !="":
                    key = keystored
                    value = valuestored

                sub_index = str("".join(text.split())).find(key.replace('"', ""))
                if sub_index >-1:
                    print(90)
                    gmt = time.gmtime()
                    ts = calendar.timegm(gmt)
                    text = ""
                    self.processValidation(key, value, line, image, image1)
                    angleSame = 1
                    r = 1
                    break
            if(angleSame ==0):
                lo = self.ang
                print(lo)
                for x in lo:
                    print (x)
                    
                    img = self.rotateBound(image, x)

                    gmt = time.gmtime()
                    ts = calendar.timegm(gmt)
                    
                    text = pytesseract.image_to_string(Image.fromarray(img),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
                    print("".join(text.split()).encode('utf8'))
                    
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
                
            if r == 0:
                str1 = " " 
                if str(str1.join(line)) != open(get_correct_path("static/uploads/_lastFail.txt")).readline().strip("\n"):
                    open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("1")
                    open(get_correct_path("static/uploads/_lastFail.txt"), "w").write(str(str1.join(line)))
                    Conveyor().closeConveyor()
                    Conveyor().enableLight("RED")
                    open(get_correct_path("static/uploads/_status.txt"), "w").write("Unit OCR Failed : Try to position the box in \n 0 or 180 degree and click Restart")
                    

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
            datacollectionValidation =json.loads(str(valid))
            calib_result_pickle = Conveyor.getScan()
            model = calib_result_pickle["model"]
            oldModel = 0
            if model != "":
                if model != str(datacollectionValidation["model"]):
                    open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("1")
                    Conveyor().closeConveyor()
                    Conveyor().enableLight("RED")
                    open(get_correct_path("static/uploads/_status.txt"), "w").write("New Model "+datacollectionValidation["model"]+" found, '\n' Close "+model+" old model pallet and Click Restart '\n' or replace model and Click Restart!")
                    oldModel = 1
            

            if oldModel == 0:
                valid = ModelValidation().validate(
                datacollectionValidation["data"], line)
                Conveyor.resetLastScan(key, value, str(datacollectionValidation["model"]))
                if(valid != '0'):
                    line = self.Reverse(line)
                    valid = ModelValidation().validate(
                        datacollectionValidation["data"], line)
                if valid !='0':
                    str1 = " " 
                    if str(str1.join(line)) != open(get_correct_path("static/uploads/_lastFail.txt")).readline().strip("\n"):
                        open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("1")
                        open(get_correct_path("static/uploads/_lastFail.txt"), "w").write(str(str1.join(line)))
                        Conveyor().closeConveyor()
                        Conveyor().enableLight("RED")
                        open(get_correct_path("static/uploads/_status.txt"), "w").write("Unit Validation Failed: Try to position the box in \n 0 or 180 degree and click Restart")
                        
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
                        
                        mdict1 = {"model": str(datacollectionValidation["model"])}
                        dict.update(mdict1)
                        mdict1 = {"customer": str(customer)}
                        dict.update(mdict1)
                        if (str(customer) == "FRONTIERC0"):
                            rtype = open(get_correct_path("static/uploads/_rtype.txt")).readline().strip("\n")
                            if rtype != "":
                                if rtype == "Field Return":
                                    type = "F"
                                if rtype == "Customer Return":
                                    type = "C"
                                if rtype == "Technical Support Return":
                                    type = "T"
                                c = c+1
                                mdict1 = {str("address"+str(c)): type}
                                dict.update(mdict1)
                        
                        line = str(dict).replace("'",'"')
                        Deepblu().postScannedSerial(line)
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

        self.title('CONTEC ARP')
        # Moved StringVar()'s to the main class
        self.loginName = tk.StringVar()
        self.loginResult = tk.StringVar()
        self.logoutButton = tk.StringVar()
        self.updatePalletId = tk.StringVar()
        open(get_correct_path("static/uploads/_login.txt"), "w").write("")

        container = tk.Frame(self)
        container.pack(side='top')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomeFrame,ScanFrame, LoginFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.configure(background='lightgrey')
            frame.grid(row=0, column=0, sticky='nswe')
        self.show_frame(HomeFrame)


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


def Close():
    answer = askokcancel(
            title='Confirmation',
            message='Do you want to close the app?',
            icon=WARNING)

    if answer:
        app.destroy()
        resetScanData()
        vs.release()

def resetScanData():
    open(get_correct_path("static/uploads/_customer.txt"), "w").write("")
    open(get_correct_path("static/uploads/_status.txt"), "w").write("")
    open(get_correct_path("static/uploads/_lastFail.txt"), "w").write("")
    open(get_correct_path("static/uploads/_rtype.txt"), "w").write("Customer Return")
    open(get_correct_path("static/uploads/_palletId.txt"), "w").write("")
    Conveyor.resetLastScan("", "", "")
    open(get_correct_path("static/uploads/_goodDataAvailable.txt"), "w").write("")
    open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("")
    open(get_correct_path("static/uploads/_serialC.txt"), "w").write("0")
def disable_event():
    pass

if __name__ == "__main__":
    global vs,vs1
    vs  = cv2.VideoCapture(Config.CAMERA_NO)
    vs .set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
    vs .set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
    vs.set(cv2.CAP_PROP_AUTOFOCUS, 0) 
    vs1  = cv2.VideoCapture(Config.CAMERA_NO)
    vs1 .set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
    vs1 .set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
    vs1 .set(cv2.CAP_PROP_AUTOFOCUS, 0) 
    app = Arp()
    app.protocol("WM_DELETE_WINDOW", disable_event)
    app.mainloop()
    MAINTENANCE_INTERVAL = .1

