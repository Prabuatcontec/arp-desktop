from config import Config
from timeit import default_timer as timer
from tkinter.constants import HORIZONTAL
import pytesseract
from numpy.lib import math
import cv2
import numpy as np
import structlog
from pyzbar import pyzbar


from datetime import datetime 
from filehandling import HoldStatus
import calendar
import random
import time
import re
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
        
        frame_eb_data = tk.Frame(self, width=100, height=10)
        frame_eb_data.grid(row=0, column=1, sticky='nsew', padx=1, pady=1)
        lab_eb_data = tk.Label(frame_eb_data, background='#DDD4EF', textvariable=controller.page1_label)
        lab_eb_data.grid(row=0, column=1)

        # frame_but_one = tk.Frame(self, width=240, height=60)
        # frame_but_one.grid(row=1, column=1, padx=1, pady=1, sticky='nsew')

        # b5 = tk.Button(frame_but_one, text='Start', command=self.callConv)
        # b5.grid(row=0, column=0, padx=1, pady=1, sticky='w')
        # b6 = tk.Button(frame_but_one, text='Stop', command=self.closeConv)
        # b6.grid(row=0, column=1, padx=1, pady=1, sticky='w')


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
        #open("static/uploads/_serial.txt", "w").write("")
        open("static/uploads/_serialUpdate.txt", "w").write("0")

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

    def callConv(self):
        Conveyor().callAllConveyor()

    def closeConv(self):
        Conveyor().CloseAllConveyor()

    def change_dropdown(self,*args):
        open("static/uploads/_customer.txt", "w").write(f"{self.category.get() }")
        #HoldStatus("").writeFile("", "_goodData")
        #open("static/uploads/_serial.txt", "w").write("")
        open("static/uploads/_status.txt", "w").write("")
        open("static/uploads/_lastFail.txt", "w").write("")
        #open("static/uploads/_lastScan.txt", "w").write("")
        open("static/uploads/_goodDataAvailable.txt", "w").write("")
        open("static/uploads/_serialUpdate.txt", "w").write("")
        open("static/uploads/_serialC.txt", "w").write("0")
        
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
    
    def videoLoop(self):
        stats = []
        start = timer()
        while not self.stopEvent.is_set():
            flag,self.frame = self.vs.read()
            if flag is None:
                print ("Failed")
            customer = open("static/uploads/_customer.txt").readline().strip("\n")
            
            
            if(customer != ""):
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
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
                if image is not None:
                    #image = cv2.imread("static/processingImg/v5/POSOSGoos_boxER_1628768871-626203.png")
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    #cv2.imwrite("static/processingImg/Real_boxER_1111111111.png" , gray)
                    
                    if(customer != ""):
                        s9 = 1
                        
                        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY   + cv2.THRESH_OTSU)[1]
                        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
                        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
                        contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                        cnt = contours
                        s = 1
                        
                        for c in cnt:
                            if(cv2.contourArea(c)  > 100000):
                                #print(cv2.contourArea(c))
                                #image = cv2.resize(thresh, (3000, 3000 ), interpolation=cv2.INTER_CUBIC)
                                serialC = open("static/uploads/_serialC.txt").readline().strip("\n")
                                if(serialC=="0"):
                                    time.sleep(.5)
                                    open("static/uploads/_serialC.txt", "w").write("1")
                                else:
                                    open("static/uploads/_serialC.txt", "w").write("0")

                                    #print(cv2.contourArea(c))
                                    rect = cv2.minAreaRect(c)
                                    box = np.int0(cv2.boxPoints(rect))

                                    [vx,vy,x,y] = box
                                    
                                    self.p = []
                                    self.p.append([x[0],x[1]+1])
                                    self.p.append([x[0]-1,vy[0]])
                                    self.p.append([y[0],y[1]])
                                    x,y,w,h = cv2.boundingRect(c)
                                    x = self.getAngel()
                                    #print(x)
                                    image = self.rotate_bound(image, x)

                                    barcodes = pyzbar.decode(image)
                                    #print(barcodes)
                                    if (len(barcodes)>0):
                                        s9 = s9 + 1
                                        break
                                
                        if s9 > 1 :
                            s = 2
                            if open("static/uploads/_serialUpdate.txt").readline().strip("\n") == "1":
                                s = 1
                            if (s > 1):
                                open("static/uploads/_serialUpdate.txt", "w").write("1")
                                
                                
                                if len(barcodes) > 0:
                                    serials = []
                                    for barcode in barcodes:
                                        barcodeData = barcode.data.decode("utf-8")
                                        if(detect_special_characer(barcodeData) == True):
                                            serials.append(barcodeData)

                                    gmt = time.gmtime()
                                    ts = calendar.timegm(gmt)
                                    fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
                                    cv2.imwrite("static/processingImg/22222222222boxER_%s.png" % fillenameImage, image)

                                    r = open("static/uploads/_goodDataAvailable.txt", "r")
                                    r = str(r.read())
                                    rev = self.Reverse(serials)
                                    if(r.find(str(serials)) !=-1 or r.find(str(rev)) != -1):
                                        open("static/uploads/_serialUpdate.txt", "w").write("0")
                                    else:
                                        if len(serials) > 1:
                                                print(serials)
                                                if s > 1:
                                                    self.processImage(serials, image, image)
                                                else:
                                                    open("static/uploads/_serialUpdate.txt", "w").write("0")

                                        else:
                                            open("static/uploads/_serialUpdate.txt", "w").write("0")
                                else:
                                    open("static/uploads/_serialUpdate.txt", "w").write("0")


    def Reverse(self, lst):
        return [ele for ele in reversed(lst)]
        

    def processImage(self, line, image, image1):
        
        r = open("static/uploads/_goodDataAvailable.txt", "r")
        r = str(r.read())
        rev = self.Reverse(line)
        if(r.find(str(line)) !=-1 or r.find(str(rev)) != -1):
            open("static/uploads/_serialUpdate.txt", "w").write("0")
            return 1
        else:
            validation = open("static/uploads/_validation.txt", 'r').read()
            #print("=============================================")
            text = pytesseract.image_to_string(Image.fromarray(image),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
            #print("".join(text.split()).encode('utf8'))
            strVal = str(validation)
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
                    r = 1
                    break
            if(angleSame ==0):
                lo = [180, -90, 90]
                for x in lo:
                    print (x)
                    
                    img = self.rotate_bound(image, x)

                    gmt = time.gmtime()
                    ts = calendar.timegm(gmt)
                    fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
                    cv2.imwrite("static/processingImg/22222222222boxER_%s.png" % fillenameImage, img)
                    
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
                
            if r == 0:
                str1 = " " 
                if str(str1.join(line)) != open("static/uploads/_lastFail.txt").readline().strip("\n"):
                    open("static/uploads/_serialUpdate.txt", "w").write("1")
                    open("static/uploads/_lastFail.txt", "w").write(str(str1.join(line)))
                    Conveyor().closeConveyor()
                    self.enableLight("RED")
                    tkinter.messagebox.askretrycancel("Unit OCR Failed", "For Units:"+ str1.join(line)+". Try to position the box in 0 or 180 degree and click retry. ")
                    self.enableLight("OFF")

                
                open("static/uploads/_serialUpdate.txt", "w").write("0")

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
                if str(str1.join(line)) != open("static/uploads/_lastFail.txt").readline().strip("\n"):
                    open("static/uploads/_serialUpdate.txt", "w").write("1")
                    open("static/uploads/_lastFail.txt", "w").write(str(str1.join(line)))
                    Conveyor().closeConveyor()
                    self.enableLight("RED")
                    tkinter.messagebox.askretrycancel("Unit Validation Failed", "Serials:"+ str1.join(line))
                    print("prabu")
                    self.enableLight("OFF")
                
                open("static/uploads/_serialUpdate.txt", "w").write("0")
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
                    customer = open("static/uploads/_customer.txt").readline().strip("\n")
                    open("static/uploads/_goodDataAvailable.txt", "a").write(str(line)+"\n")
                    
                    mdict1 = {"model": str(jsonArray["model"])}
                    dict.update(mdict1)
                    mdict1 = {"customer": str(customer)}
                    dict.update(mdict1)
                    line = str(dict).replace("'",'"')
                    requests.post(Config.DEEPBLU_URL + '/autoreceive/automation', line,
                                        headers={'Content-Type': 'application/json', 
                                        'Authorization': 'Basic QVVUT1JFQ0VJVkU6YXV0b0AxMjM=' }
                                        )
                    print('success')
                    self.enableLight("GREEN")
                    open("static/uploads/_serialUpdate.txt", "w").write("0")
                    Conveyor().callConveyor()
                    start = time.time()
                    print(start)
            
    def enableLight(self, state):
        res1 = requests.post(
            Config.API_MOTOR_URL + 'devices/4', data=json.dumps({"state": state}),
            headers={'Content-Type': 'application/json'}
        )
        print(res1)

    
    


class Arp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

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
    MAINTENANCE_INTERVAL = .1

