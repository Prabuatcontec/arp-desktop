from config import Config
from timeit import default_timer as timer
from tkinter.constants import HORIZONTAL
import pytesseract
from numpy.lib import math
import cv2
import numpy as np
from pyzbar import pyzbar
import time
import re
import os
import json
import threading
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
#import newrelic
#import newrelic.agent


class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        # Home Frame #
        tk.Frame.__init__(self, parent)
        
        frameButRight = tk.Frame(self, width=1000, height=2)
        frameButRight.grid(row=0, column=0, padx=1, pady=1, sticky='nsew')
       
        # Login Button #
        buttonEntryData = tk.Button(frameButRight, text="Login", background='#59981A', width=10, height=2,  command=lambda: controller.show_frame(LoginFrame))
        buttonEntryData.grid(row=0, column=0)
        # Close Button #
        buttonEntryData = tk.Button(frameButRight, text="Close", width=10, height=2, background='#D10000',  command=Close)
        buttonEntryData.grid(row=0, column=1)
      

class ScanFrame(tk.Frame):
    # Scan Frame #
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        global on, frame, lbx
        frameEntryData = tk.Frame(self, width=100, height=10)
        frameEntryData.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)

         # Select Customer #
        self.customerSelect = tk.StringVar()
        somechoices = []
        for value in Connection().getCustomer():
           somechoices.append(value[2])

        
        self.customerSelect.set("Pick a Customer")

        popupMenu = tk.OptionMenu(frameEntryData, self.customerSelect, *somechoices)
        popupMenu.grid(row=0, column=0)

        self.customerSelect.trace('w', self.chooseCustomer)

        # Return Type #
        self.returnType = tk.StringVar()
        frame = tk.Frame(self, width=240, height=10)
        frame.grid(row=1, column=0, pady=3, sticky='nsew')

        frame._grid_info = frame.grid_info()
        frame.grid_remove()
        somechoices = ["Field Return", "Customer Return", "Technical Support Return"]
        popupMenu1 = tk.OptionMenu(frame, self.returnType, *somechoices)
        self.returnType.set("Customer Return")
        popupMenu1.grid(row=0, column=0, pady=3)
        self.returnType.trace('w', self.returnTypeSelect)

        # Pallet 
        entryNombreEntry = tk.Entry(frameEntryData)
        entryNombreEntry.config(textvariable=controller.updatePalletId, relief='flat')
        entryNombreEntry.grid(row=0, column=1, sticky='w')
        

        # Close Pallet Button #
        buttonEntryData = tk.Button(frameEntryData, text="Close Pallet", width=10, height=2, background='#D10000',  command=self.ClosePallet)
        buttonEntryData.grid(row=1, column=1, pady=3)

        # Pallet Scanned Count Title #
        frameEntryModelFrame = tk.Frame(self, width=100, height=10)
        frameEntryModelFrame.grid(row=0, column=2, sticky='nsew', padx=20, pady=1)
        frameEntryModel = tk.Label(frameEntryModelFrame, foreground='#C32148', textvariable=self.controller.palletSerialCountTitle, font=(None, 12))
        frameEntryModel.grid(row=0, column=0)

        # Pallet Scanned Count #
        frameEntryModel = tk.Label(frameEntryModelFrame, foreground='#C32148', textvariable=self.controller.palletSerialCount, font=(None, 15))
        frameEntryModel.grid(row=0, column=1)

        frameEntryModel = tk.Label(frameEntryModelFrame, foreground='#C32100', textvariable=self.controller.modelNameTitle, font=(None, 12))
        frameEntryModel.grid(row=0, column=2)
        frameEntryModel = tk.Label(frameEntryModelFrame, foreground='#C32100', textvariable=self.controller.modelName, font=(None, 15))
        frameEntryModel.grid(row=0, column=3)

        # Restart Button #
        frameButtonOne = tk.Frame(self, width=100, height=10)
        frameButtonOne.grid(row=1, column=3, sticky='nsew', padx=3)
        restartButton = tk.Button(frameButtonOne, bg='#18A558', text='Restart', height=2, command=self.removeStatus)
        restartButton.grid(row=0, column=0)
        

        frameEntryData = tk.Frame(self, width=100, height=10)
        frameEntryData.grid(row=0, column=4, sticky='nsew', padx=1, pady=1)
        # Login Name Display #
        labData = tk.Label(frameEntryData, foreground="#810541" ,  textvariable=controller.loginName, font=(None, 20))
        labData.grid(row=0, column=0)

        # Logout #
        frameButRight = tk.Frame(self, width=240, height=10)
        frameButRight.grid(row=0, column=6, padx=20, pady=1, sticky='nsew')

        # Manual Scan Button #
        buttonEntryData = tk.Button(frameButRight, text="Manual", width=10, height=2, background='#D10000',  command=self.loadPopup)
        buttonEntryData.grid(row=0, column=0, padx = 10)

        buttonEntryData = tk.Button(frameButRight, text="Logout", width=10, height=2, background='#FFA500',  command=lambda: controller.show_frame(LoginFrame))
        buttonEntryData.grid(row=0, column=1)

        # Close Button #
        buttonEntryData = tk.Button(frameButRight, text="Close", width=10, height=2, background='#D10000',  command=self.Close)
        buttonEntryData.grid(row=0, column=2, padx = 10)

        # Maximum Pallet Count #
        frameEntryData = tk.Frame(self, width=100, height=10)
        frameEntryData.grid(row=0, column=5, sticky='nsew', padx=1, pady=1)

        labData = tk.Label(frameEntryData, foreground="#C32100" ,  text="Max Count:")
        labData.grid(row=0, column=0)

        entryNombreEntry = tk.Entry(frameEntryData)
        entryNombreEntry.grid(row=0, column=1, sticky='w')
        
        entryNombreEntry.config(textvariable=controller.palletMaxCount, relief='flat')
        entryNombreEntry.grid(row=0, column=1)

        


        # Video Frame #
        frameVideo = tk.Frame(self, colormap="new")
        frameVideo.grid(row=3, column=0, padx=20, pady=1, sticky='e')
        frameVideoOne = tk.Frame(self, colormap="new")
        frameVideoOne.grid(row=3, column=1, padx=20, pady=1, sticky='e')
        
        self.stopEvent = None
        self.stopEventOne = None
        self.frame = frameVideo
        self.frame1 = frameVideoOne

        self.videoStream  = cv2.VideoCapture(Config.CAMERA_NO)
        self.videoStream.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
        self.videoStream.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
        self.videoStream.set(cv2.CAP_PROP_AUTOFOCUS, 0) 
        self.videoStreamOne  = cv2.VideoCapture(Config.CAMERA_NO_TWO)
        self.videoStreamOne.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
        self.videoStreamOne.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
        self.videoStreamOne.set(cv2.CAP_PROP_AUTOFOCUS, 0) 

        self.scanned = ""
        self._serialC = 0
        self._serialUpdate = 0
        self._customer = ""
        self._goodDataAvailable = ""
        self._lastFail = ""
        self._status = ""
        self._validation = ""
        self.scannedcount = 0
        self._failedCount = 0
        self.controller.palletSerialCount.set(self.scannedcount)
        self.controller.modelNameTitle.set("Model:")
        self.controller.modelName.set("None")
        self.controller.palletSerialCountTitle.set("Scanned:")
        self.controller.palletMaxCount.set(0)
        self.cam = ""
        self.stopEvent = True
        self.stopEventOne = True
        self.thread = threading.Thread(target=self.videoCheck, args=())
        self.thread.start()
        self.panel = None
        self.panel1 = None
        self.top = None
        self._rType = "Customer Return"
        
        self.p = []
        self.ang = []
        #self.bg_task()

    # @newrelic.agent.background_task() 
    # def bg_task(self):
    #     # do some type of work in this background task...
    #     application = newrelic.agent.application()
    #     #application = newrelic.agent.register_application(timeout=10)
    #     result = newrelic.agent.record_custom_event('ArpDetrash', {'pallet':'ARP1213133123'}, application)
    #     print(result)
    # Close button on scan screen #
    def Close(self):
        answer = askokcancel(
            title='Confirmation',
            message='Do you want to close the app?',
            icon=WARNING)

        if answer:
            self.videoStream.release()
            self.videoStreamOne.release()
            self.destroy()
            Close()
    
    # Manual Popup #
    def loadPopup(self):
        
        if self._customer == "":
            showinfo(
                title='Select Customer',
                message='Choose Customer before try Manual',
            icon=WARNING)
        else :
            if self.top != None:
                self.top.destroy()
            top = self.top = tk.Toplevel(self)
            img = tk.Image("photo", file=getCorrectPath("static/uploads/manual.png"))
            top.tk.call('wm','iconphoto',top._w, img)
            self.top.geometry("%dx%d%+d%+d" % (500, 400, 10, 50))
            postData = {}
            for value in Connection().getModels(self._customer):
                appData = {value[1]:value[2]}
                postData.update(appData)
            _customerModels = json.dumps(postData)

            #self._validation =  json.loads(self._validation)

            self.model = tk.StringVar()
            self.dc = tk.StringVar()
            frameme = tk.Frame(top, width=340, height=30)
            frameme.grid(row=2, column=0, padx=1, pady=20, sticky='nsew')
            frameme.pack()
            somechoices = json.loads(_customerModels)
            popupMenu1 = tk.OptionMenu(frameme, self.model, *somechoices)
            self.model.trace('w', self.chooseModel)

            modelDataDetail = Conveyor.getScan()
            model = modelDataDetail["model"]
            value = modelDataDetail["value"]
            if model != "":
                self.model.set(model)
                self.dc.set(value)
            else:
                self.model.set("Select Model")
            popupMenu1.grid(row=2, column=2,
               ipady=6)

            self.serials = []
            self.cnt = 0
            self.scannedValue = ""
            self.selectedKey = ""
            self.selectedValue = ""
            
            self.myLabel = tk.Label(top, text='Scan label')
            self.myLabel.pack(pady=4)
            self.sv = tk.StringVar()
            self.outputDisplay = tk.StringVar()
            self.outputDisplay.set("")
            self.sv.trace("w",  self.scanData)
            self.myEntryBox = tk.Entry(top, textvariable = self.sv, font=(None, 20))

            self.myEntryBox.focus()
            self.myEntryBox.pack(
               ipady=8)

            self.myEntryLabel = tk.Label(top, height=2, textvariable=self.outputDisplay)
            self.myEntryLabel.pack(pady=2)

            self.closeButton = tk.Button(top, height=2, text='Close', command=self.ClosePopup)
            self.closeButton.pack()

            # Manual Serial Entry #
            self.smyLabelAcc = tk.Label(top, text='')
            self.smyLabelAcc.pack(padx=6, pady=2)
            self.myLabelAcc = tk.Label(top, text='Manual Entry')
            self.myLabelAcc.pack()
            self.myEntryBoxacc = tk.Entry(top, font=(None, 20))
            self.myEntryBoxacc.pack(
               ipady=8)

            
            threading.Thread(target=self.scannedValueAdded, daemon=True).start()
       

    # Choose Model #
    def chooseModel(self,*args):
        if (self.model.get() != "Select Model"):
            self.selectedKey = self.model.get()

            strVal = str(self._validation)
            models = json.loads(strVal)
            
            for key, value in models.items():
                if self.selectedKey == key:
                    self.selectedValue = value
                    break
            
            self.serials = []
            self.outputDisplay.set("")
            self.dc.set(self.selectedValue)
        
 
    # Close popup #   
    def ClosePopup(self):
        self.top.destroy()

    # Remove Duplicate #
    def duplicateremove(self, x):
      return list(dict.fromkeys(x))
    
    # Get Scanned Serial #
    def scanData(self, *args):
        self.scannedValue = self.myEntryBox.get()
        self.cnt = time.time()
    
    # Add scanned value to array #
    def scannedValueAdded(self):
        while True:
            lo=threading.Lock()
            lo.acquire()
            if(time.time() - self.cnt>.5 and self.cnt>0 and self.scannedValue!=""):
                self.cnt=0
                self.serials.append(self.scannedValue)
                self.serials = self.duplicateremove(self.serials)
                self.sv.set("")
            if len(self.serials) > 0:
                self.outputDisplay.set(str(self.serials))
                if str(self.dc.get()) != "":
                    datacollectionValidation =json.loads(str(self.dc.get()))
                    isExist = str(datacollectionValidation['model']).find("NVG")

                    lengthCnt = len(datacollectionValidation['data'])
                    if isExist >-1:
                        lengthCnt = 3
                    if lengthCnt == len(self.serials):
                        self.postManualData(self.serials,  datacollectionValidation)
            time.sleep(.5)
            lo.release()


    # Manual Post to deepblu #
    def postManualData(self, line, datacollectionValidation):
        isExist = str(datacollectionValidation['model']).find("NVG")
        accsLine = ""
        if isExist >-1:
            accsLine = line[2]
            line.pop()
        
        
        self.serials = []
        validDc = ModelValidation().validate(
                        datacollectionValidation["data"], line)
        if validDc == '0':
            postData = {}
            for c in range(len(line)):
                newline = line[c].replace("\n","").replace(" ","")
                
                if(c == 0):
                    appData = {"serial": newline}
                    postData.update(appData)
                else:
                    appData = {str("address"+str(c)): newline}
                    postData.update(appData)


            
            customer = self._customer
            
            appData = {"model": str(datacollectionValidation['model'])}
            postData.update(appData)
            appData = {"customer": str(customer)}
            postData.update(appData)
            appData = {"stationId": str(Config.STATION_ID)}
            postData.update(appData)
            user = open(getCorrectPath("static/uploads/_login.txt")).readline().strip("\n")
            appData = {"adduser": str(user)}
            postData.update(appData)
            appData = {"source": "DeTrash"}
            postData.update(appData)
            if (str(customer) == "FRONTIERC0"):

                if accsLine != "":
                    c = c+1
                    appData = {str("address"+str(c)): accsLine}
                    postData.update(appData)
                rtype = self._rType
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
            line = str(postData).replace("'",'"')
            response = Deepblu().postScannedSerial(line)
            if response.status_code == 201:
                self.outputDisplay.set("Posted!!!")
                Conveyor().callConveyor()
                print('success')
                self.scanned = ""
                self._serialUpdate = 0
                self._status = ""
                self._lastFail = ""
                self.scannedcount = self.scannedcount + 1
                self.controller.palletSerialCount.set(self.scannedcount)
            else:
                result = response.json()
                print(result)
                resultType = result['type']
                
                if resultType == 3:
                    self.outputDisplay.set("Deepblu Failed : Serial is already received 3 times")
        else:
            self.outputDisplay.set("Datacollection Validation Fails")
    

    # Rotate Image #
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

    # Converting Video frame to array #
    def getImgArray(self, image):
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        return image

    def videoCheck(self):
        while True:
            if self.cam == "" or self.cam == "0":
                self.stopEvent = True
                self.stopEventOne = False
                self.videoLoop()
            if self.cam == "" or self.cam == "1":
                self.stopEvent = False
                self.stopEventOne = True
                self.videoLoopOne()
    
    # Camera One Video Frame Process #
    def videoLoop(self):
        while self.stopEvent == True:
            customer = self._customer
            if self.videoStream is None or not self.videoStream.isOpened():
                image = self.camNotAvailable("CAM 1 NOT AVAILABLE", "0")
                frameimage = image
                readFrame = image
            else:
                flag,readFrame = self.videoStream.read()
                dim = Config.CAMERA_FRAME_LEN
                self.frame = cv2.resize(readFrame, dim, interpolation = cv2.INTER_AREA)
                
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
            self.processFrame(image, customer, "0")

    # Show Status Message #
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
    
    # Camera two Video Frame Process #
    def videoLoopOne(self):
        while self.stopEventOne == True:
            customer = self._customer
            if self.videoStreamOne is None or not self.videoStreamOne.isOpened():
                image = self.camNotAvailable("CAM 1 NOT AVAILABLE", "0")
                frameimage = image
                readFrame = image
            else:
                flag,readFrame = self.videoStreamOne.read()
                dim = Config.CAMERA_FRAME_LEN
                self.frame1 = cv2.resize(readFrame, dim, interpolation = cv2.INTER_AREA)
                
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
            self.processFrame(image, customer, "1")
    
    # Camera Availability Check #
    def camNotAvailable(self, alert, imgId):
        if imgId == "0":
            image = cv2.imread(getCorrectPath("static/uploads/cam.png"))
        else:
            image = cv2.imread(getCorrectPath("static/uploads/customer1.jpg"))
        image = cv2.resize(image, Config.CAMERA_FRAME_LEN, interpolation = cv2.INTER_AREA)
        cv2.putText(image, alert, (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.5, 255, 5)
        return image
    
    # Process Frame to validate barcode #
    def processFrame(self,image, customer, cam):
        if cam == "1":
            self.stopEvent = True
            self.stopEventOne = False
        if cam == "0":
            self.stopEventOne = True
            self.stopEvent = False
        if image is not None:
            #image = cv2.imread("static/processingImg/1.png")
            if(customer != ""):
                if int(self.controller.palletMaxCount.get()) == int(self.scannedcount) and int(self.controller.palletMaxCount.get()) > 0:
                    Conveyor().enableLight("RED")
                    self.scanned = ""
                    self._serialUpdate = 1
                    self._status = "Pallet Max Count reached"
                    return 1
                if cam == "1":
                    #camera1  roate and read the barcode
                    self.ang = [-90, 90]
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
                            i = i - 1
                            if(int(cv2.contourArea(c))  == an[0]):
                                if(self._serialC == 0 ):
                                    #time.sleep(.1)
                                    self._serialC = 1
                                else:
                                    self._serialC = 0

                                    rect = cv2.minAreaRect(c)
                                    box = np.int0(cv2.boxPoints(rect))
                                    [vx,vy,x,y] = box
                    
                                    self.p = []
                                    self.p.append([x[0],x[1]+1])
                                    self.p.append([x[0]-1,vy[0]])
                                    self.p.append([y[0],y[1]])
                                    x,y,w,h = cv2.boundingRect(c)
                                    
                                    barcodes = pyzbar.decode(image)

                                    serials = []
                                    for barcode in barcodes:
                                        barcodeData = barcode.data.decode("utf-8")
                                        barcodeType = barcode.type
                                        if(detectSpecialCharacer(barcodeData) == True):
                                            serials.append(barcodeData)

                                    if len(serials)<1:
                                        x = self.getAngel()
                                        image = self.rotateBound(image, x)
                                        barcodes = pyzbar.decode(image)
                                        serials = []
                                        for barcode in barcodes:
                                            barcodeData = barcode.data.decode("utf-8")
                                            barcodeType = barcode.type
                                            if(detectSpecialCharacer(barcodeData) == True):
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
                        # cv2.imwrite(getCorrectPath("static/processingImg/111Bfrrot1boxER_%s.png") % fillenameImage, image)
                        rev = self.Reverse(serials)
                        
                        validateDuplicate = self.checkDuplicate(serials, rev)
                        if validateDuplicate == 1:
                            return 1
                        if len(serials) > 0:
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

    # Array Reverse #
    def Reverse(self, lst):
        return [ele for ele in reversed(lst)]
    
    # Check String has int"
    def checkIfStringIsInt(self,string1):
        for character in string1:
            if not character.isdigit():
                return "0"
        else:
            return "1"
    
    # Check QRCode Serial with Space #
    def getQRCodeSerials(self, value):
        serials = []
        isExist = str("".join(value)).find("\n")
        if isExist >-1:
            splitSerialSpace = value.split("\n")
            serials.append(splitSerialSpace[0])
            serials.append(splitSerialSpace[1])
            return serials
        return serials

    # Get Bhr4 Serials #
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
    
    # Check Serial is been scanned again #
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
        

    # Process the Frame and Validate Dc #
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
            validation = open(getCorrectPath("static/uploads/_bhr4.txt"), 'r').read()
            strVal = str(validation)
            models = json.loads(strVal)
            for key, value in models.items():
                modelDataDetail = Conveyor.getScan()
                keystored = modelDataDetail["key"]
                valuestored = modelDataDetail["value"]
                if keystored != "" and valuestored !="":
                    key = keystored
                    value = valuestored
                self.processValidation(key, value, line, "BHR4", cam, barcodeData)
                r = 1
        else:
            validation = self._validation
            text = pytesseract.image_to_string(Image.fromarray(image),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
            #print("".join(text.split()).encode('utf8'))
            strVal = str(validation)
            models = json.loads(strVal)
            angleSame = 0
            
            for key, value in models.items():
                modelDataDetail = Conveyor.getScan()
                keystored = modelDataDetail["key"]
                valuestored = modelDataDetail["value"]
                
                if keystored != "" and valuestored !="":
                    findNvg = keystored.split("NVG448B")
                    if(len(findNvg)<=1):
                        key = keystored
                        value = valuestored

                
                isExist = str("".join(text.split())).find(key.replace('"', ""))
                if isExist >-1:
                    #print(90)
                    isExist = str(key.replace('"', "")).find("NVG")
                    if isExist >-1 and len(line)<2:
                        sn = self.findSN(text)
                        mac = self.findMac(text)
                        intCheck = self.checkIfStringIsInt(line[0])
                        if intCheck == "0":
                            line.append(sn)
                        if intCheck == "1":
                            line.append(mac)
                        
                    self.processValidation(key, value, line, text, cam, barcodeData)
                    text = ""
                    angleSame = 1
                    r = 1
                    break
            if(angleSame ==0):
                lo = self.ang
                # Rotate Frame and fins the OCR #
                for x in lo:
                    #print (x)
                    validateDuplicate = self.checkDuplicate(line, rev)
                    if validateDuplicate == 1:
                        break
                    img = self.rotateBound(image, x)
                    text = pytesseract.image_to_string(Image.fromarray(img),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
                    #print("".join(text.split()).encode('utf8'))
                    # gmt = time.gmtime()
                    # ts = calendar.timegm(gmt)
                    # fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
                    # cv2.imwrite(getCorrectPath("static/processingImg/An111Bfrrot1boxER_%s.png") % fillenameImage, img)
                    
                    for key, value in models.items():
                        isExist = str("".join(text.split())).find(key.replace('"', ""))
                        if isExist >-1:
                            
                            isExist = str(key.replace('"', "")).find("NVG")
                            if isExist >-1 and len(line)<2:
                                sn = self.findSN(text)
                                mac = self.findMac(text)
                                intCheck = self.checkIfStringIsInt(line[0])
                                if intCheck == "0":
                                    line.append(sn)
                                if intCheck == "1":
                                    line.append(mac)

                            line = self.Reverse(line)
                            self.processValidation(key, value, line, text, cam, barcodeData)
                            text = ""
                            r = 1
                            break
                    if r == 1:
                        break
            
        if r == 0:#
            str1 = " " 
            if str(str1.join(line)) != self._lastFail:
                if self._failedCount > 0 :
                    self.scanned = ""
                    self._serialUpdate = 1
                    self._failedCount = 0
                    self._lastFail = str(str1.join(line))
                    Conveyor().enableLight("RED")
                    self._status = "Unit OCR Failed : Try to position the box in \n 0 or 180 degree and click Restart"
                else:
                    self._failedCount = 1
                

    def gradiant(self,p1,p2):
        cal =  (p1[1]-p2[1])/(p2[0]-p1[0])
        return cal

    # Get Angel to rotate image to read OCR #
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

    # Processing Datacollection Validation #
    def processValidation(self, key, value, line, text, cam, barcodeData):
            dataLine = barcodeData
            validData = str(value).replace("'",'"')
            datacollectionValidation =json.loads(str(validData))
            modelDataDetail = Conveyor.getScan()
            model = modelDataDetail["model"]
            oldModel = 0
            if model != "":
                if model != str(datacollectionValidation["model"]):
                    self.scanned = ""
                    self._serialUpdate = 1
                    Conveyor().enableLight("RED")
                    self._status = "New Model "+datacollectionValidation["model"]+" found, '\n' Close "+model+" old model pallet and Click Restart '\n' or replace model and Click Restart!"
                    oldModel = 1
            

            if oldModel == 0:
                validDc = ModelValidation().validate(
                datacollectionValidation["data"], line)
                Conveyor.resetLastScan(key, value, str(datacollectionValidation["model"]))

                # Check 
                if(validDc != '0'):
                    line = self.Reverse(line)
                    validDc = ModelValidation().validate(
                        datacollectionValidation["data"], line)
                if validDc !='0':
                    str1 = " " 
                    if str(str1.join(line)) != self._lastFail:
                        if self._failedCount > 0 :
                            self.scanned = ""
                            self._serialUpdate = 1
                            self._failedCount = 0
                            self._lastFail = str(str1.join(line))
                            Conveyor().enableLight("RED")
                            self._status = "Unit Validation Failed: Try to position the box in \n 0 or 180 degree and click Restart"
                        else:
                            self._failedCount = 1
                            
                    return 1

                if validDc == '0':
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
                        user = open(getCorrectPath("static/uploads/_login.txt")).readline().strip("\n")
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
                                    return 1
                                    

                            rtype = self._rType
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
                            str1 = " " 
                            if str(str1.join(dataLine)) == self._goodDataAvailable:
                                self._serialUpdate = 0
                                self._goodDataAvailable = str(str1.join(dataLine))
                            else:
                                self._goodDataAvailable = str(str1.join(dataLine))
                                response = Deepblu().postScannedSerial(line)
                                if response.status_code == 201:
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
                                    
                                elif response.status_code == 400:
                                    result = response.json()
                                    resultType = result['type']
                                    self._serialUpdate = 0
                                    if resultType == 3:
                                        Conveyor().enableLight("RED")
                                        self.scanned = ""
                                        self._serialUpdate = 1
                                        self._status = "Deepblu Failed : Serial is already received 3 times"
                                    else:
                                        self._serialUpdate = 0
                                    if resultType == 1:
                                        Conveyor().enableLight("RED")
                                        self.scanned = ""
                                        self._serialUpdate = 1
                                        self._status = "Deepblu Failed : Serial is already in Deepblu"
                                else:
                                    Conveyor().enableLight("RED")
                                    self.scanned = ""
                                    self._serialUpdate = 1
                                    self._status = "Deepblu Connection Failed"

    # Get Access Code for NVG Model from OCR text #
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

    # Read the SN if it fails in barcode for NVG #
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
    
    # Read the Mac if it fails in barcode for NVG #
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

    # Set return type for Frontiet #
    def returnTypeSelect(self, *args):
        self._rType = self.returnType.get()

    # Reset when unit fails#
    def removeStatus(self):
        self._status = ""
        self._lastFail = ""
        self._serialUpdate = 0
        Conveyor().enableLight("OFF")

    # Select Customer #
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

        # Thread to run and
        threading.Thread(target=self.getCurrentPalletId, daemon=True).start()
        
      
    # Get Pallet Id from Deepblu #
    def getCurrentPalletId(self):
        """ Background thread doing various Pallet Id tasks """
        while True:
            l=threading.Lock()
            l.acquire()
            modelDataDetail = Conveyor.getScan()
            model = modelDataDetail["model"]
            if model != "":
                self.controller.modelName.set(model)
                response = Deepblu().getPalletId(model)
                if response.status_code != 200:
                    self.controller.loginResult.set("Deepblu Pallet Falied!")
                else:
                    a = response.json()
                    if len(a)>0:
                        self.controller.updatePalletId.set(a[0]['palletId'])
                        open(getCorrectPath("static/uploads/_palletId.txt"), "w").write(str(a[0]['palletId']))

            time.sleep(10)
            l.release()

    # Close pallet action once pallet Built #
    def ClosePallet(self):
        answer = askokcancel(
            title='Confirmation',
            message='Do you want to close the pallet?',
            icon=WARNING)

        if answer:
            response = Deepblu().closePallet()
            if response.status_code != 200:
                self.controller.loginResult.set("Deepblu Pallet Close Falied!")
            else:
                self.scanned = ""
                self._serialC = 0
                self._serialUpdate = 0
                self._goodDataAvailable = ""
                self._lastFail = ""
                self._status = ""
                self.cam = ""
                self.stopEvent = True
                self.stopEventOne = True
                self.scannedcount = 0
                self.controller.palletSerialCount.set(self.scannedcount)
                self.controller.modelName.set("NONE")
                self.controller.modelNameTitle.set("Model:")
                self.controller.palletSerialCountTitle.set("Scanned:")
                palletDetail = response.json()
                Deepblu().printPalletTag(palletDetail)
                Conveyor.resetLastScan("", "", "")
                self._goodDataAvailable = "" 

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        frameUpLeft = tk.Frame(self, width=1000, height=10,   colormap="new")
        frameUpLeft.grid(row=0, column=0, sticky='w', padx=1, pady=1)
        frameUpLeftOne = tk.Frame(self, width=200, height=10,   colormap="new")
        frameUpLeftOne.grid(row=1, column=0, sticky='w', padx=1, pady=1)
        frameButton = tk.Frame(self, width=200, colormap="new")
        frameButton.grid(row=2, column=0, padx=1, pady=1, sticky='w')

        
        loginButton = tk.Button(frameButton, text='Login', width=10, height=2, background='#59981A',  command= self.login)
        loginButton.grid(row=0, column=0, padx=1, pady=1, sticky='w')
        
        buttonEntryData = tk.Button(frameButton, text="Close", width=10, height=2, background='#D10000',  command=Close)
        buttonEntryData.grid(row=0,padx=1, pady=3, column=1)

        

        self.entryNombreFld = tk.Entry(frameUpLeft, width=25)
        self.entryNombreFld.grid(row=0, column=1, sticky='w')
        self.entry_nombre_fld1 = tk.Entry(frameUpLeftOne, width=25,  show='*')
        self.entry_nombre_fld1.grid(row=0, column=1, sticky='w')
        labelTwo = tk.Label(frameUpLeft, text="Username:", font=("bold", 14))
        labelTwo.grid(row=0, column=0, sticky='w')
        labelThree = tk.Label(frameUpLeftOne, text="Password: ", font=("bold", 14))
        labelThree.grid(row=0, column=0, sticky='w')
        labData = tk.Label(frameButton, foreground='#D10000', textvariable=self.controller.loginResult)
        labData.grid(row=3, column=0, columnspan=2)

     # update the loginName in login Sucess #
    def login(self):
        response = requests.post(
        Config.API_USER_URL + 'users/login', data=json.dumps({"username": self.entryNombreFld.get(), "password": self.entry_nombre_fld1.get(), "Site": "Matamoros"}),
        headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            self.controller.loginResult.set("Authentication Failed!")
        else:
            self.controller.loginName.set(self.entryNombreFld.get().upper())
            open(getCorrectPath("static/uploads/_login.txt"), "w").write(f"{self.entryNombreFld.get() }")
            self.controller.logoutButton.set("Logout")
            self.controller.show_frame(ScanFrame)



class Arp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('CONTEC ARP')
        # Moved StringVar()'s to the main class
        self.loginName = tk.StringVar()
        self.modelName = tk.StringVar()
        self.modelNameTitle = tk.StringVar()
        self.loginResult = tk.StringVar()
        self.palletSerialCount = tk.StringVar()
        self.palletSerialCountTitle = tk.StringVar()
        self.logoutButton = tk.StringVar()
        self.updatePalletId = tk.StringVar()
        self.palletMaxCount = tk.StringVar()
        open(getCorrectPath("static/uploads/_login.txt"), "w").write("")
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
        self.show_frame(LoginFrame)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

def detectSpecialCharacer(pass_string):
    regex= re.compile("'")
    if(regex.search(pass_string) != None): 
        return False
    regex= re.compile('[@_!#$%^&*()<>?/\\\|}{~:[\]]"') 
    if(regex.search(pass_string) == None): 
        res = True
    else:
        res = False
    return(res)

def getCorrectPath(relative_path):
    p = os.path.abspath(".").replace('/dist', "")
    return os.path.join(p, relative_path)


def Close():
    app.destroy()

def resetScanData():
    open(getCorrectPath("static/uploads/_customer.txt"), "w").write("")
    open(getCorrectPath("static/uploads/_status.txt"), "w").write("")
    open(getCorrectPath("static/uploads/_lastFail.txt"), "w").write("")
    open(getCorrectPath("static/uploads/_rtype.txt"), "w").write("Customer Return")
    open(getCorrectPath("static/uploads/_palletId.txt"), "w").write("")
    Conveyor.resetLastScan("", "", "")
    open(getCorrectPath("static/uploads/_goodDataAvailable.txt"), "w").write("")
    open(getCorrectPath("static/uploads/_serialUpdate.txt"), "w").write("")
    
def disable_event():
    pass

if __name__ == "__main__":
    #newrelic.agent.initialize('newrelic.ini')
    global vs,vs1,lastScan
    app = Arp()
    app.protocol("WM_DELETE_WINDOW", disable_event)
    img = tk.Image("photo", file=getCorrectPath("static/uploads/auto.png"))
    app.tk.call('wm','iconphoto',app._w, img)
    app.mainloop()
    MAINTENANCE_INTERVAL = .1
    

