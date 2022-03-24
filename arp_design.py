from config import Config
from timeit import default_timer as timer
from tkinter.constants import END, HORIZONTAL, X
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
from tkinter.messagebox import ERROR, askokcancel, showerror, showinfo, WARNING
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
      

class ScanFrame(tk.Canvas):
    # Scan Frame #
    def __init__(self, parent, controller):
        tk.Canvas.__init__(self, parent)
        self.controller = controller
        global on, frame, lbx
        
        self.logobgimg = tk.PhotoImage(
        file=getCorrectPath("assets/blue/logo.png"))
        self.logobg = self.create_image(
            0,
            0,
            image=self.logobgimg,anchor='ne'
        )

        self.loginButtonReal1 = tk.Button(
            image=self.logobgimg,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat", cursor="hand1"
        )
        self.loginButtonReal1.place(
            x=30,
            y=30,
            width=105.0,
            height=90.0
        )
        self.barDiv = tk.PhotoImage(
        file=getCorrectPath("assets/blue/bar.png"))
        self.barButtonOne = tk.Button(
            image=self.barDiv,
            borderwidth=0,
            highlightthickness=0,
            relief="flat" 
        )
        self.barButtonOne.place(
            x=1620.0,
            y=10.0,
            width=14.0,
            height=120.0
        )

        self.barDiv4 = tk.PhotoImage(
        file=getCorrectPath("assets/blue/Line.png"))
        self.barButtonOne1 = tk.Button(
            image=self.barDiv4,
            borderwidth=0,
            highlightthickness=0,
            relief="flat" 
        )
        self.barButtonOne1.place(
            x=955.0,
            y=200.0,
            width=14.0,
            height=750.0
        )

        self.loginButton = tk.PhotoImage(
        file=getCorrectPath("assets/blue/Close.png"))
        self.loginButtonReal = tk.Button(
            image=self.loginButton,
            borderwidth=0,
            highlightthickness=0,
            command=self.ClosePallet,
            relief="flat", cursor="hand1"
        )
        self.loginButtonReal.place(
            x=1510.0,
            y=26.0,
            width=95.0,
            height=50.0
        )

        
        self.barButton = tk.Button(
            image=self.barDiv,
            borderwidth=0,
            highlightthickness=0,
            relief="flat" 
        )
        self.barButton.place(
            x=1280.0,
            y=10.0,
            width=14.0,
            height=120.0
        )


        self.palletIdPic = tk.PhotoImage(
        file=getCorrectPath("assets/blue/PalletEntry.png"))
        self.palletIdPicbg = self.create_image(
            1520.0,
            21.0,
            image=self.palletIdPic,anchor='ne'
        )
 

        self.palletIdEntry = tk.Entry(
            bd=0,
            bg="#E6E6E6",
            fg="#5B5B52",
            highlightthickness=0,
            textvariable=controller.updatePalletId
        )
        self.palletIdEntry.place(
            x=1342.0,
            y=25.0,
            width=148.0,
            height=38.0
        )

        self.palletMaxCnt = tk.PhotoImage(
        file=getCorrectPath("assets/blue/palletmax.png"))
        self.palletMaxCntbg = self.create_image(
            1481.0,
            80.0,
            image=self.palletMaxCnt,anchor='ne'
        )
 

        self.palletMaxCntEntry = tk.Entry(
            bd=0,
            bg="#E6E6E6",
            fg="#5B5B52",
            highlightthickness=0,
            textvariable=controller.palletMaxCount
        )
        self.palletMaxCntEntry.place(
            x=1421.0,
            y=83.0,
            width=40.0,
            height=28.0
        )

        self.mxtLblCnt = tk.Label(bd=0,bg='#3A7FF6',fg='#FFFFFF', textvariable="Max Cnt: ", text="Max Cnt: ", font=(None, 15))
        self.mxtLblCnt.place( x=1320.0,
            y=82.0,
            width=90.0,
            height=35.0)

        self.loginButtonManual = tk.PhotoImage(
        file=getCorrectPath("assets/blue/Manual.png"))
        self.loginButtonManualReal = tk.Button(
            image=self.loginButtonManual,
            borderwidth=0,
            highlightthickness=0,
            command=self.loadPopup,
            relief="flat", cursor="hand1"
        )
        self.loginButtonManualReal.place(
            x=1480.0,
            y=80.0,
            width=120.0,
            height=50.0
        )

        self.usernameimg = tk.PhotoImage(
        file=getCorrectPath("assets/blue/entry1.png"))
        self.usernameimgbg = self.create_image(
            1825.0,
            5.0,
            image=self.usernameimg,anchor='ne'
        )

        self.usernamelog = tk.Entry(
            bd=0,
            bg="#E6E6E6",
            fg="#5B5B52",
            highlightthickness=0
        )
        self.usernamelog.insert(0, 'Username')
        self.usernamelog.place(
            x=1685.0,
            y=10.0,
            width=125.0,
            height=30.0
        )

        self.usernamelog.bind("<Button-1>", lambda event: clear_entry(event, self.usernamelog))


        self.passwordimg = tk.PhotoImage(
        file=getCorrectPath("assets/blue/entry2.png"))
        self.passwordimgbg = self.create_image(
            1827.0,
            50.0,
            image=self.passwordimg,anchor='ne'
        )
        self.passwordlog = tk.Entry(
            bd=0,
            bg="#E6E6E6",
            fg="#5B5B52",
            show='*',
            highlightthickness=0
        )
        self.passwordlog.insert(0, 'Password')
        self.passwordlog.place(
            x=1687.0,
            y=53.0,
            width=125.0,
            height=30.0
        )
        self.passwordlog.bind("<Button-1>", lambda event: clear_entry(event, self.passwordlog))


        self.loginButtonw = tk.PhotoImage(
        file=getCorrectPath("assets/blue/login.png"))
        self.loginButtonReal = tk.Button(
            image=self.loginButtonw,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat", cursor="hand1"
        )
        self.loginButtonReal.place(
            x=1665.0,
            y=100.0,
            width=145.0,
            height=50.0
        )

        self.mxtLblCnt = tk.Label(bd=0,bg='#3A7FF6',fg='#FFFFFF', textvariable="Count: ", text="Count: ", font=(None, 15))
        self.mxtLblCnt.place( x=1070.0,
            y=6.0,
            width=70.0,
            height=33.0)

        self.palletMaxCnts = tk.PhotoImage(
        file=getCorrectPath("assets/blue/palletmax.png"))
        self.palletMaxCntbg = self.create_image(
            1210.0,
            5.0,
            image=self.palletMaxCnts,anchor='ne'
        )
        self.palletMaxCntEntry = tk.Entry(
            bd=0,
            bg="#E6E6E6",
            fg="#5B5B52",
            highlightthickness=0,
            textvariable=self.controller.palletSerialCount
        )
        self.palletMaxCntEntry.place(
            x=1152.0,
            y=7.0,
            width=40.0,
            height=30.0
        )


        self.mxtLblCnt = tk.Label(bd=0,bg='#3A7FF6',fg='#FFFFFF', textvariable="Model: ", text="Model: ", font=(None, 15))
        self.mxtLblCnt.place( x=1069.0,
            y=48.0,
            width=70.0,
            height=35.0)

        self.palletMaxModel = tk.PhotoImage(
        file=getCorrectPath("assets/blue/Model.png"))
        self.palletMaxCntbg = self.create_image(
            1235.0,
            54.0,
            image=self.palletMaxModel,anchor='ne'
        )

        self.palletMaxCntEntry = tk.Entry(
            bd=0,
            bg="#E6E6E6",
            fg="#5B5B52",
            highlightthickness=0,
            textvariable=self.controller.modelName
        )
        self.palletMaxCntEntry.place(
            x=1145.0,
            y=60.0,
            width=70.0,
            height=25.0
        )


        

        self.restartButton = tk.PhotoImage(
        file=getCorrectPath("assets/blue/Restart.png"))
        self.restartButtonReal = tk.Button(
            image=self.restartButton,
            borderwidth=0,
            highlightthickness=0,
            command=self.removeStatus,
            relief="flat", cursor="hand1"
        )
        self.restartButtonReal.place(
            x=1100.0,
            y=95.0,
            width=120.0,
            height=50.0
        )


         
 
        self.palletCustomerReturn = tk.PhotoImage(
        file=getCorrectPath("assets/blue/Return.png"))
        
        
        # Return Type #
        self.returnType = tk.StringVar()
       
       
        somechoices = ["Field Return", "Customer Return", "Technical Support Return"]
        self.popupMenu1 = tk.OptionMenu(self, self.returnType, *somechoices)
        self.returnType.set("Customer Return")
        self.popupMenu1.configure(bg="#E7E7E7",fg="#5B5B52",bd=0,highlightthickness=0)
        self.popupMenu1.place(
            x=875.0,
            y=70.0,
            width=0,
            height=0
        )
        self.returnType.trace('w', self.returnTypeSelect)
 
        # Video Frame #
        frameVideo = tk.Frame(self, colormap="new",background="#FFFFFF")
        frameVideo.grid(row=3, column=0, padx=20, pady=1, sticky='e')
        frameVideoOne = tk.Frame(self, colormap="new",background="#FFFFFF")
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
        self.loginName = ""
        
        self.p = []
        self.ang = []
        #self.bg_task()
 
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
            frameme = tk.Frame(top, width=340, height=30,background="#3A7FF6")
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

    def login(self):
        response = requests.post(
        Config.API_USER_URL + 'users/login', data=json.dumps({"username": self.usernamelog.get(), "password": self.passwordlog.get(), "Site": "Matamoros"}),
        headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            self.controller.loginResult.set("Authentication Failed!")
            
        else:
            result = response.json()
            username = result['user']['fullName']
            self.controller.loginName.set(username)
            open(getCorrectPath("static/uploads/_login.txt"), "w").write(f"{self.usernamelog.get() }")
            self.controller.logoutButton.set("Logout")
            self.controller.show_frame(ScanFrame)
            self.usernamelog.place(width=0,height=0)
            self.passwordlog.place(width=0,height=0)
            self.loginButtonReal.place(width=0,height=0)
            self.delete(self.usernameimgbg)
            self.delete(self.passwordimgbg)
            self.loginName = username

            self.mxtLblCnts = tk.Label(bd=0,bg='#3A7FF6',fg='#FFFFFF', textvariable=self.controller.loginName, text=self.controller.loginName, font=(None, 15))
            self.mxtLblCnts.place( x=1707.0,
                y=35.0,
                width=100.0,
                height=35.0)
            
            self.logoutButtonw = tk.PhotoImage(
            file=getCorrectPath("assets/blue/Logout.png"))
            self.loginButtonReal = tk.Button(
                image=self.logoutButtonw,
                borderwidth=0,
                highlightthickness=0,
                command=self.Close,
                relief="flat", cursor="hand1"
            )
            self.loginButtonReal.place(
                x=1667.0,
                y=80.0,
                width=145.0,
                height=50.0
            )

            self.profileButtonw = tk.PhotoImage(
            file=getCorrectPath("assets/blue/Profile.png"))
            self.profileButtonReal = tk.Button(
                image=self.profileButtonw,
                borderwidth=0,
                highlightthickness=0,
                command=self.Close,
                relief="flat", cursor="hand1"
            )
            self.profileButtonReal.place(
                x=1680.0,
                y=30.0,
                width=50.0,
                height=45.0
            )


        self.barDiv1 = tk.PhotoImage(
        file=getCorrectPath("assets/blue/bar.png"))
        self.barButtonOne = tk.Button(
            image=self.barDiv1,
            borderwidth=0,
            highlightthickness=0,
            relief="flat" 
        )
        self.barButtonOne.place(
            x=1055.0,
            y=10.0,
            width=14.0,
            height=120.0
        )

        self.palletCustomer = tk.PhotoImage(
        file=getCorrectPath("assets/blue/Customer.png"))
        self.palletMaxCntbg = self.create_image(
            1045.0,
            8.0,
            image=self.palletCustomer,anchor='ne'
        )

        

        self.customerSelect = tk.StringVar()
        somechoices = []
        for value in Connection().getCustomer():
           somechoices.append(value[2])

        
        self.customerSelect.set("Pick a Customer")

        self.popupMenu = tk.OptionMenu( self, self.customerSelect, *somechoices)
        self.popupMenu.configure(bg="#E7E7E7",fg="#5B5B52",bd=0,highlightthickness=0)
        self.popupMenu.place(
            x=875.0,
            y=14.0,
            width=160.0,
            height=35.0
        )
        self.customerSelect.trace('w', self.chooseCustomer)

            

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
        self._serialUpdate = ""
        self.cam = ""
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
                self.palletMaxCntbg = self.create_image(
                1053.0,
                65.0,
                image=self.palletCustomerReturn,anchor='ne'
            )
                self.popupMenu1.place(
                    x=885.0,
                    y=70.0,
                    width=150.0,
                    height=35.0
                )
            else:
                self.popupMenu1.place(
                    x=0,
                    y=0,
                    width=0,
                    height=0
                )

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


def clear_entry(event, entry):
    entry.delete(0, END)
    entry.unbind('<Button-1>')



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

 
        container = tk.Canvas(self)
        container.pack(side='top',fill=X,ipady =50)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        

        self.frames = {}
        for F in (HomeFrame,ScanFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.configure(background='#3A7FF6')
            frame.grid(row=0, column=0, sticky='nswe')
        self.show_frame(ScanFrame)


    def show_frame(self, cont):
        frame = self.frames[cont]
        tk.Misc.lift(frame)

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
    #app.wm_attributes('-fullscreen', 'True')
    app.geometry("1800x1024")
    app.configure(bg = "#FFF")
    app.mainloop()
    MAINTENANCE_INTERVAL = .1
    

