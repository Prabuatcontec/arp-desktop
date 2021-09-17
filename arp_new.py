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
from tkinter import ttk  

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
        frame_eb_data = tk.Frame(self, width=1000, height=10)
        frame_eb_data.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
        lab_eb_data = tk.Label(frame_eb_data, foreground="#810541" ,  textvariable=controller.loginName)
        lab_eb_data.grid(row=0, column=0)
        entry_nombre_fld1c = tk.Entry(frame_eb_data)
        entry_nombre_fld1c.grid(row=0, column=1, sticky='w')

        entry_nombre_fld1c.config(textvariable=controller.updatePalletId, relief='flat')
        entry_nombre_fld1c.grid(row=0, column=2)

        frame_but_one = tk.Frame(self, width=240, height=10)
        frame_but_one.grid(row=0, column=1, padx=20, pady=1, sticky='nsew')

        b5 = tk.Button(frame_but_one, bg='#18A558', text='Restart', height=2, command=self.removeStatus)
        b5.grid(row=0, column=1, padx=20, pady=1, sticky='w')

        
        frame_eb_model = tk.Frame(self, width=100, height=10)
        frame_eb_model.grid(row=0, column=2, sticky='nsew', padx=20, pady=1)
        lab_eb_model = tk.Label(frame_eb_model, foreground='#C32148', textvariable=self.controller.modelNameTit, font=(None, 15))
        lab_eb_model.grid(row=0, column=1)

        frame_eb_model = tk.Frame(self, width=100, height=10)
        frame_eb_model.grid(row=0, column=3, sticky='nsew', padx=2, pady=1)
        lab_eb_model = tk.Label(frame_eb_model, foreground='#C32148', textvariable=self.controller.modelName, font=(None, 20))
        lab_eb_model.grid(row=0, column=1)

        frame_eb_model = tk.Frame(self, width=100, height=10)
        frame_eb_model.grid(row=0, column=4, sticky='nsew', padx=20, pady=1)
        lab_eb_model = tk.Label(frame_eb_model, foreground='#C32148', textvariable=self.controller.palletSerialCountTit, font=(None, 15))
        lab_eb_model.grid(row=0, column=1)

        frame_eb_model = tk.Frame(self, width=100, height=10)
        frame_eb_model.grid(row=0, column=5, sticky='nsew', padx=2, pady=1)
        lab_eb_model = tk.Label(frame_eb_model, foreground='#C32148', textvariable=self.controller.palletSerialCount, font=(None, 20))
        lab_eb_model.grid(row=0, column=1)

        frame_but_right = tk.Frame(self, width=240, height=10)
        frame_but_right.grid(row=0, column=6, padx=20, pady=1, sticky='nsew')
        b_ebdata = tk.Button(frame_but_right, text="Logout", width=10, height=2, background='#FFA500',  command=lambda: controller.show_frame(HomeFrame))
        b_ebdata.grid(row=0, column=0, padx = 100)
        b_ebdata = tk.Button(frame_but_right, text="Close", width=10, height=2, background='#D10000',  command=Close)
        b_ebdata.grid(row=0, column=1, padx = 100)

        self.model = tk.StringVar()
        frame = tk.Frame(self, width=240, height=10)
        frame.grid(row=1, column=0, padx=20, pady=1, sticky='nsew')

        frame._grid_info = frame.grid_info()
        frame.grid_remove()
        somechoices = ["Field Return", "Customer Return", "Technical Support Return"]
        popupMenu1 = tk.OptionMenu(frame, self.model, *somechoices)
        self.model.set("Customer Return")
        popupMenu1.grid(row=1, column=0)
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


       
        
        frame_video = tk.Frame(self, colormap="new")
        frame_video.grid(row=3, column=0, padx=20, pady=1, sticky='e')
        frame_video1 = tk.Frame(self, colormap="new")
        frame_video1.grid(row=3, column=1, padx=20, pady=1, sticky='e')
        
        self.stopEvent = None
        self.frame = frame_video
        self.frame1 = frame_video1

        self.scanned = ""
        self._serialC = 0
        self._serialUpdate = 0
        self._customer = ""
        self._goodDataAvailable = ""
        self._lastFail = ""
        self._status = ""
        self._validation = ""
        self.scannedcount = 0
        self.controller.palletSerialCount.set(self.scannedcount)
        self.controller.modelNameTit.set("Model:")
        self.controller.modelName.set("None")
        self.controller.palletSerialCountTit.set("Scanned:")
        
        #vs = VideoStream(0)
        self.cam = ""
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        self.thread = threading.Thread(target=self.videoLoopOne, args=())
        self.thread.start()
        self.panel = None
        self.panel1 = None
        
        self.p = []
        self.ang = []


   
            
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

    def getImgArray(self, image):
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        return image
    
    def videoLoop(self):
        stats = []
        start = timer()
        while not self.stopEvent.is_set():
            if self.cam == "" or self.cam == "0":
                #print(self.cam)
                customer = self._customer
                if vs is None or not vs.isOpened():
                    image = self.camNotAvailable("CAM 1 NOT AVAILABLE", "0")
                    frameimage = image
                    readFrame = image
                else:
                    flag,readFrame = vs.read()
                    dim = (800, 800)
                    self.frame = cv2.resize(readFrame, dim, interpolation = cv2.INTER_AREA)
                    if flag is None:
                        print ("Failed")
                    
                    if(customer != ""):
                        image = cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)
                        frameimage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                        frameimage = self.alertProcess(frameimage)
                    else:
                        image = self.camNotAvailable("CONTEC ARP", "1")
                        frameimage = image
                        readFrame = image

                image = self.getImgArray(image)
                frameimage = self.getImgArray(frameimage)
        
                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = tk.Label(image=frameimage)
                    self.panel.image = frameimage
                    self.panel.pack(side="left", padx=10, pady=10)
        
                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=frameimage)
                    self.panel.image = frameimage

                image = readFrame
                self.ProcessCam(image, customer, "0")

    def alertProcess(self, frameimage):
        _status = self._status
        y0, dy = 50, 50
        isExist = _status.find("New")
        if isExist >-1:
            colr = (255, 165, 0)
        else:
            colr = (255, 0, 0)
        isExist = _status.find("received")
        if isExist >-1:
            colr = (255,99,71)
        

        if _status != "":
            for i, line in enumerate(_status.split('\n')):
                y = y0 + (i*dy)
                cv2.putText(frameimage, line.replace('\n', ""), (50, y), cv2.FONT_HERSHEY_SIMPLEX, 1, colr, 5)
        
        return frameimage
        
    def videoLoopOne(self):
        stats = []
        start = timer()
        while not self.stopEvent.is_set():
            if self.cam == "" or self.cam == "1":
                #print(self.cam)
                customer = self._customer
                if vs1 is None or not vs1.isOpened():
                    image = self.camNotAvailable("CAM 1 NOT AVAILABLE", "0")
                    frameimage = image
                    readFrame = image
                else:
                    flag,readFrame = vs1.read()
                    dim = (800, 800)
                    self.frame1 = cv2.resize(readFrame, dim, interpolation = cv2.INTER_AREA)
                    if flag is None:
                        print ("Failed")
                    
                    if(customer != ""):
                        image = cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)
                        frameimage = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2RGB)
                        frameimage = self.alertProcess(frameimage)
                    else:
                        image = self.camNotAvailable("CONTEC ARP", "1")
                        frameimage = image
                        readFrame = image

                image = self.getImgArray(image)
                frameimage = self.getImgArray(frameimage)
        
                # if the panel is not None, we need to initialize it
                if self.panel1 is None:
                    self.panel1 = tk.Label(image=frameimage)
                    self.panel1.image = frameimage
                    self.panel1.pack(side="left", padx=10, pady=10)
        
                # otherwise, simply update the panel
                else:
                    self.panel1.configure(image=frameimage)
                    self.panel1.image = frameimage

                image = readFrame
                self.ProcessCam(image, customer, "1")
    
    def camNotAvailable(self, alert, imgId):
        if imgId == "0":
            image = cv2.imread(get_correct_path("static/uploads/cam.png"))
        else:
            image = cv2.imread(get_correct_path("static/uploads/customer1.jpg"))
        image = cv2.resize(image, (1000,1000), interpolation = cv2.INTER_AREA)
        cv2.putText(image, alert, (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.5, 255, 5)
        return image
    
    def variance_of_laplacian(self, image):
        # compute the Laplacian of the image and then return the focus
        # measure, which is simply the variance of the Laplacian
        return cv2.Laplacian(image, cv2.CV_64F).var()

    def ProcessCam(self,image, customer, cam):
        if image is not None:
            image = cv2.imread("static/processingImg/1.png")
            if(customer != ""):
                print(cam)
                if cam == "1":
                    #camera1  roate and read the barcode
                    self.ang = [-90, 90,  180]
                    image = self.rotateBound(image, 90)
                else:
                    self.ang = [180, 90, -90]
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
                barcodeType = None
                if len(an)>0:
                    
                    for c in cnt:
                        if(cv2.contourArea(c)  > 100000):
                            #print(cv2.contourArea(c))
                            i = i - 1
                            if(int(cv2.contourArea(c))  == an[0]):
                                
                                #serialC = "1"
                                print('self')
                                print(self._serialC)
                                if(self._serialC == 0 ):
                                    time.sleep(2)
                                    self._serialC = 1
                                else:
                                    self._serialC = 0

                                    print(cv2.contourArea(c))
                                    rect = cv2.minAreaRect(c)
                                    box = np.int0(cv2.boxPoints(rect))
                                    [vx,vy,x,y] = box
                    
                                    self.p = []
                                    self.p.append([x[0],x[1]+1])
                                    self.p.append([x[0]-1,vy[0]])
                                    self.p.append([y[0],y[1]])
                                    x,y,w,h = cv2.boundingRect(c)
                                    
                                    barcodes = pyzbar.decode(image)
                                    print(barcodes)

                                    serials = []
                                    for barcode in barcodes:
                                        barcodeData = barcode.data.decode("utf-8")
                                        barcodeType = barcode.type
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
                                            barcodeType = barcode.type
                                            if(detect_special_characer(barcodeData) == True):
                                                serials.append(barcodeData)

                                        if (len(serials)>0):
                                            s9 = s9 + 1
                                            
                                            break
                                    else:
                                        s9 = s9 + 1
                                        break
                            
                            if (len(an) == i):
                                break
                            if po == 1:
                                break

                
                if s9 > 1 :
                    start = time.time()
                    print("Start")
                    print(start)
                    s = 2
                    if self._serialUpdate == 1:
                        s = 1
                    if (s > 1):
                        self._serialUpdate = 1
                        # gmt = time.gmtime()
                        # ts = calendar.timegm(gmt)
                        # fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
                        # cv2.imwrite(get_correct_path("static/processingImg/111Bfrrot1boxER_%s.png") % fillenameImage, image)
                        rev = self.Reverse(serials)
                        
                        validateDuplicate = self.checkDuplicate(serials, rev)
                        if validateDuplicate == 1:
                            return 1
                        if len(serials) > 0:
                                #print(serials)
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
                                            break

                                    self.processImage(serials, t, image, cam, barcodeType)
                                else:
                                    self._serialUpdate = 0

                        else:
                            self._serialUpdate = 0
                else:
                    self._serialUpdate = 0


    def Reverse(self, lst):
        return [ele for ele in reversed(lst)]
    
    def check_if_string_is_int(self,string1):
        for character in string1:
            if not character.isdigit():
                return "0"
        else:
            return "1"
    
    def getQRCodeSerials(self, value):
        
        splitSerial = value.split(";")
        print(splitSerial)
        serials = []
        isExist = str("".join(value)).find("\n")
        if isExist >-1:
            splitSerialSpace = value.split("\n")
            serials.append(splitSerialSpace[0])
            serials.append(splitSerialSpace[1])
            return serials
        return serials

    def getBhr4Serials(self, value):
        
        splitSerial = value.split(";")
        serials = []
        
        if len(splitSerial) == 1:
            return serials
        if len(splitSerial) == 0:
            return serials
        
        if len(splitSerial) < 12:
            
            wifi = splitSerial[0].split('WIFI:S:')
            wpa = splitSerial[2].split('P:')
            router = splitSerial[4].split('ROUTER:S:')
            cm = '012345ABCDEF'
            pws = splitSerial[7].split('P:')
            serials.append(router[1])
            serials.append(cm)
            serials.append(pws[1])
            serials.append(wifi[1])
            serials.append(wpa[1])
            
        else :
            wifi = splitSerial[0].split('WIFI:S:')
            wpa = splitSerial[2].split('P:')
            router = splitSerial[4].split('ROUTER:S:')
            cm = splitSerial[6].split('M:')
            pws = splitSerial[9].split('P:')
            
            serials.append(router[1])
            serials.append(cm[1])
            serials.append(pws[1])
            serials.append(wifi[1])
            serials.append(wpa[1])
        return serials
    
    def checkDuplicate(self, serial, reverse):
        str1 = " " 
        
        if str(str1.join(serial)) == self._lastFail:
            self._serialUpdate = 0
            return 1
                                
        str1 = " " 
        if str(str1.join(reverse)) == self._lastFail:
            self._serialUpdate = 0
            return 1
        
        goodDataAvailable = self._goodDataAvailable
        str1 = " " 
        if str(str1.join(serial)) == goodDataAvailable:
            self._serialUpdate = 0
            return 1
        
        str1 = " " 
        if str(str1.join(reverse)) == goodDataAvailable:
            self._serialUpdate = 0
            return 1
        
        return 0
        

    def processImage(self, line, image, image1, cam, barcodeType):
        barcodeData = line
        if barcodeType == 'QRCODE':
            line = self.getBhr4Serials(line[0])
            if len(line) == 0:
                barcodeType = ""
                line = barcodeData

            
        rev = self.Reverse(line)
       
        validateDuplicate = self.checkDuplicate(line, rev)
        if validateDuplicate == 1:
            return 1


        r = 0
        if barcodeType == 'QRCODE':
            print(barcodeType)
            validation = open(get_correct_path("static/uploads/_bhr4.txt"), 'r').read()
            strVal = str(validation)
            models = json.loads(strVal)
            print(models)
            for key, value in models.items():
                print(key)
                print(value)
                calib_result_pickle = Conveyor.getScan()
                keystored = calib_result_pickle["key"]
                valuestored = calib_result_pickle["value"]
                if keystored != "" and valuestored !="":
                    key = keystored
                    value = valuestored
                self.processValidation(key, value, line, image, "BHR4", cam, barcodeData)
                r = 1
        else:
            validation = self._validation
            text = pytesseract.image_to_string(Image.fromarray(image),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
            #print("".join(text.split()).encode('utf8'))
            strVal = str(validation)
            models = json.loads(strVal)
            angleSame = 0
            
            for key, value in models.items():
                calib_result_pickle = Conveyor.getScan()
                keystored = calib_result_pickle["key"]
                valuestored = calib_result_pickle["value"]
                if keystored != "" and valuestored !="":
                    key = keystored
                    value = valuestored
                
                isExist = str("".join(text.split())).find(key.replace('"', ""))
                if isExist >-1:
                    #print(90)
                    isExist = str(key.replace('"', "")).find("NVG")
                    if isExist >-1 and len(line)<2:
                        sn = self.findSN(text)
                        mac = self.findMac(text)
                        intCheck = self.check_if_string_is_int(line[0])
                        if intCheck == "0":
                            line.append(sn)
                        if intCheck == "1":
                            line.append(mac)
                        
                    self.processValidation(key, value, line, image, text, cam, barcodeData)
                    text = ""
                    angleSame = 1
                    r = 1
                    break
            if(angleSame ==0):
                lo = self.ang
                #print(lo)
                for x in lo:
                    print (x)
                    validateDuplicate = self.checkDuplicate(line, rev)
                    if validateDuplicate == 1:
                        break
                    img = self.rotateBound(image, x)
                    text = pytesseract.image_to_string(Image.fromarray(img),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
                    #print("".join(text.split()).encode('utf8'))
                    # gmt = time.gmtime()
                    # ts = calendar.timegm(gmt)
                    # fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
                    # cv2.imwrite(get_correct_path("static/processingImg/An111Bfrrot1boxER_%s.png") % fillenameImage, img)
                    
                    for key, value in models.items():
                        isExist = str("".join(text.split())).find(key.replace('"', ""))
                        if isExist >-1:
                            
                            isExist = str(key.replace('"', "")).find("NVG")
                            if isExist >-1 and len(line)<2:
                                
                                sn = self.findSN(text)
                                mac = self.findMac(text)
                                intCheck = self.check_if_string_is_int(line[0])
                                if intCheck == "0":
                                    line.append(sn)
                                if intCheck == "1":
                                    line.append(mac)
                                #print("--------------------------Line-----------------------")
                                #print(line)

                            line = self.Reverse(line)
                            #print(line)
                            self.processValidation(key, value, line, img, text, cam, barcodeData)
                            text = ""
                            r = 1
                            break
                    if r == 1:
                        break
            
        if r == 0:
            str1 = " " 
            if str(str1.join(line)) != self._lastFail:
                self.scanned = ""
                self._serialUpdate = 1
                self._lastFail = str(str1.join(line))
                Conveyor().enableLight("RED")
                self._status = "Unit OCR Failed : Try to position the box in \n 0 or 180 degree and click Restart"
                

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

    def processValidation(self, key, value, line, image, text, cam, barcodeData):
            dataLine = barcodeData
            #print(value)
            valid = str(value).replace("'",'"')
            datacollectionValidation =json.loads(str(valid))
            calib_result_pickle = Conveyor.getScan()
            model = calib_result_pickle["model"]
            oldModel = 0
            if model != "":
                if model != str(datacollectionValidation["model"]):
                    self.scanned = ""
                    self._serialUpdate = 1
                    #Conveyor().closeConveyor()
                    Conveyor().enableLight("RED")
                    self._status = "New Model "+datacollectionValidation["model"]+" found, '\n' Close "+model+" old model pallet and Click Restart '\n' or replace model and Click Restart!"
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
                    if str(str1.join(line)) != self._lastFail:
                        self.scanned = ""
                        self._serialUpdate = 1
                        self._lastFail = str(str1.join(line))
                        Conveyor().enableLight("RED")
                        self._status = "Unit Validation Failed: Try to position the box in \n 0 or 180 degree and click Restart"
                        
                    return 1

                if valid == '0':
                    postData = {}
                    p = 0
                    for c in range(len(line)):
                        newline = line[c].replace("\n","").replace(" ","")
                        
                        if(c == 0):
                            appData = {"serial": newline}
                            postData.update(appData)
                        else:
                            appData = {str("address"+str(c)): newline}
                            postData.update(appData)

                    if(p == 0):
                        customer = self._customer
                        
                        appData = {"model": str(datacollectionValidation["model"])}
                        postData.update(appData)
                        appData = {"customer": str(customer)}
                        postData.update(appData)
                        appData = {"stationId": str(Config.STATION_ID)}
                        postData.update(appData)
                        user = open(get_correct_path("static/uploads/_login.txt")).readline().strip("\n")
                        appData = {"adduser": str(user)}
                        postData.update(appData)
                        appData = {"source": "DeTrash"}
                        postData.update(appData)
                        failedAccessCode = "1"
                        if (str(customer) == "FRONTIERC0"):
                            isExist = str(key.replace('"', "")).find("NVG")
                            if isExist >-1:
                                accessCode = self.findAccessCode(text.replace("UL",""))
                                if(accessCode != "0"):
                                    c = c+1
                                    appData = {str("address"+str(c)): accessCode}
                                    postData.update(appData)
                                else:
                                    failedAccessCode = "0"
                                    self.scanned = ""
                                    self._serialUpdate = 1
                                    Conveyor().enableLight("RED")
                                    self._status = "NVG Failed for access Code: Try to  \n position the box in  0 or 180 degree and click Restart"
                                    

                            rtype = open(get_correct_path("static/uploads/_rtype.txt")).readline().strip("\n")
                            if rtype != "":
                                if rtype == "Field Return":
                                    type = "F"
                                if rtype == "Customer Return":
                                    type = "C"
                                if rtype == "Technical Support Return":
                                    type = "T"
                                c = c+1
                                appData = {str("address"+str(c)): type}
                                postData.update(appData)
                        if failedAccessCode == "1":
                            line = str(postData).replace("'",'"')
                            print(line)
                            str1 = " " 
                            if str(str1.join(dataLine)) == self._goodDataAvailable:
                                self._serialUpdate = 0
                                self._goodDataAvailable = str(str1.join(dataLine))
                            else:
                                self._goodDataAvailable = str(str1.join(dataLine))
                                response = Deepblu().postScannedSerial(line)
                                print(response.status_code)
                                if response.status_code == 201:
                                    print("con start")
                                    start = time.time()
                                    print(start)
                                    Conveyor().callConveyor()
                                    print('success')
                                    self.scanned = ""
                                    self.cam = cam
                                    self._serialUpdate = 0
                                    self._status = ""
                                    self._lastFail = ""
                                    self.scannedcount = self.scannedcount + 1
                                    self.controller.palletSerialCount.set(self.scannedcount)
                                    start = time.time()
                                    print(start)
                                else:
                                    result = response.json()
                                    resultType = result['type']
                                    print(resultType)
                                    self._serialUpdate = 0
                                    if resultType == 3:
                                        Conveyor().enableLight("RED")
                                        self.scanned = ""
                                        self._serialUpdate = 1
                                        self._status = "Deepblu Failed : Serial "+line[0]+" is already received 3 times"
                                    else:
                                        self._serialUpdate = 0
                                    if resultType == 1:
                                        Conveyor().enableLight("RED")
                                        self.scanned = ""
                                        self._serialUpdate = 1
                                        self._status = "Deepblu Failed : Serial "+line[0]+" is already in Deepblu"
                                    else:
                                        self._serialUpdate = 0

    def findAccessCode(self, text):
        text = str(" ".join(text.split()))
        findNvg = text.split("DAC")
       
        if(len(findNvg)<2):
            return "0"

        if(len(findNvg)>1):
            findNvg = re.findall("\d+", findNvg[1])
            if len(findNvg)>0:
                if(len(findNvg[0])<10):
                    return "0"
                else:
                    return findNvg[0]
            else:
                return "0"
        return "0"


    def findSN(self, text):
        text = str(" ".join(text.split()))
        findNvg = text.split("SN")
        if(len(findNvg)<2):
            return "0"

        if(len(findNvg)>1):
            findNvg = re.findall("\d+", findNvg[1])
            if len(findNvg)>0:
                if(len(findNvg[0])>14):
                    return findNvg[0]
                else:
                    return "0"
            else:
                return "0"
        return "0"
    
    def findMac(self, text):
        text = str(" ".join(text.split()))
        findNvg = text.split("MACA")
       
        if(len(findNvg)<2):
            return "0"
        
        findN = findNvg[1]
        findNs = findN.split("ADC")
        
        if(len(findNs)>0):
            datas = re.sub(r"[^A-Z0-9]","",findNs[0])
            return datas[-12:] 

        return "0"

    def grid_hide(self, widget):
        widget._grid_info = widget.grid_info()
        widget.grid_remove()

    def grid_show(self, widget):
        widget.grid(**widget._grid_info)


    def ReturnTypeSelect(self, *args):
        open(get_correct_path("static/uploads/_rtype.txt"), "w").write(f"{self.model.get()}")

    def callConv(self):
        Conveyor().callAllConveyor()

    def removeStatus(self):
        self._status = ""
        self._lastFail = ""
        self._serialUpdate = ""
        Conveyor().enableLight("OFF")

    def closeConv(self):
        Conveyor().CloseAllConveyor()

    def chooseCustomer(self,*args):
        resetScanData()
        self._customer = self.customerSelect.get()
        
        postData = {}
        for value in Connection().getModels(self.customerSelect.get()):
           appData = {value[1]:value[2]}
           postData.update(appData)
        self._validation = json.dumps(postData)
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
                self.controller.modelName.set(model)
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
                self.scanned = ""
                self._serialC = 0
                self._serialUpdate = 0
                self._goodDataAvailable = ""
                self._lastFail = ""
                self._status = ""
                self._validation = ""
                self.scannedcount = 0
                self.controller.palletSerialCount.set(self.scannedcount)
                self.controller.modelName.set("NONE")
                self.controller.modelNameTit.set("Model:")
                self.controller.palletSerialCountTit.set("Scanned:")
                palletDetail = response.json()
                Deepblu().printPalletTag(palletDetail)
                Conveyor.resetLastScan("", "", "")
                self._goodDataAvailable = ""
                
                

        


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



class Arp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('CONTEC ARP')
        # Moved StringVar()'s to the main class
        self.loginName = tk.StringVar()
        self.modelName = tk.StringVar()
        self.modelNameTit = tk.StringVar()
        self.loginResult = tk.StringVar()
        self.palletSerialCount = tk.StringVar()
        self.palletSerialCountTit = tk.StringVar()
        self.logoutButton = tk.StringVar()
        self.updatePalletId = tk.StringVar()
        open(get_correct_path("static/uploads/_login.txt"), "w").write("")
        resetScanData()

        container = tk.Frame(self)
        container.pack(side='top')
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        

        self.frames = {}
        for F in (HomeFrame,ScanFrame, LoginFrame):
            frame = F(container, self)
            self.frames[F] = frame
            #frame.configure(background='lightgrey')
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
        vs1.release()

def resetScanData():
    open(get_correct_path("static/uploads/_customer.txt"), "w").write("")
    open(get_correct_path("static/uploads/_status.txt"), "w").write("")
    open(get_correct_path("static/uploads/_lastFail.txt"), "w").write("")
    open(get_correct_path("static/uploads/_rtype.txt"), "w").write("Customer Return")
    open(get_correct_path("static/uploads/_palletId.txt"), "w").write("")
    Conveyor.resetLastScan("", "", "")
    open(get_correct_path("static/uploads/_goodDataAvailable.txt"), "w").write("")
    open(get_correct_path("static/uploads/_serialUpdate.txt"), "w").write("")
    
def disable_event():
    pass

if __name__ == "__main__":
    global vs,vs1,lastScan
    vs  = cv2.VideoCapture(Config.CAMERA_NO)
    vs .set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
    vs .set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
    vs.set(cv2.CAP_PROP_AUTOFOCUS, 0) 
    vs1  = cv2.VideoCapture(Config.CAMERA_NO_TWO)
    vs1 .set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
    vs1 .set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
    vs1 .set(cv2.CAP_PROP_AUTOFOCUS, 0) 
    app = Arp()
    app.protocol("WM_DELETE_WINDOW", disable_event)
    app.mainloop()
    MAINTENANCE_INTERVAL = .1

