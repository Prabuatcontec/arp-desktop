from config import Config
from timeit import default_timer as timer
from tkinter.constants import HORIZONTAL

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
import tkinter as tk
import imutils
from PIL import Image
from PIL import ImageTk
from imutils.video import VideoStream
from mysql import Connection
from tkinter.ttk import Progressbar
import requests



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
        frame_but_right.grid(row=2, column=1, padx=1, pady=1, sticky='nsew')
        b_ebdata = tk.Button(frame_but_right, text="Logout", width=10, height=2, command=lambda: controller.show_frame(PageOne))
        b_ebdata.grid(row=2, column=1)
        self.category = tk.StringVar()
        somechoices = []
        for value in Connection().getCustomer():
           somechoices.append(value[2])

        #somechoices = ["1", "2", "C", "D"]
        self.category.set("Pick a category")
        open("static/uploads/_customer.txt", "w").write("")
        open("static/uploads/_serial.txt", "w").write("")

        popupMenu = tk.OptionMenu(frame_eb_data, self.category, *somechoices)
        popupMenu.grid(row=1, column=1)
        self.category.trace('w', self.change_dropdown)
        self.progress = Progressbar(frame_eb_data, orient=HORIZONTAL,length=100,  mode='indeterminate')

    def change_dropdown(self,*args):
        print( self.category.get() )
        HoldStatus("").writeFile("", "_lastScan")
        HoldStatus("").writeFile("0", "_lastScanCount")
        HoldStatus("").writeFile("2", "_scan")
        HoldStatus("").writeFile("0", "_serialpostCount")
        HoldStatus("").writeFile("", "_goodData")
        HoldStatus("").writeFile("0", "_processing")
        
        dict = {}
        self.progress.grid(row=2,column=0)
        self.progress.start()
        for value in Connection().getModels(self.category.get()):
           mdict1 = {value[1]:value[2]}
           dict.update(mdict1)
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
            # do things...
            time.sleep(.5)
            readText.readData()
            
            

    def postingData(self):
        """ Background thread doing various maintenance tasks """
        readText = ImageProcess()
        while True:
            # do things...
            time.sleep(.5)
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
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
                gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
                gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

                # subtract the y-gradient from the x-gradient
                gradient = cv2.subtract(gradX, gradY)
                gradient = cv2.convertScaleAbs(gradient)

                # blur and threshold the image
                blurred = cv2.blur(gradient, (9, 9))
                (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)   

                coords = np.column_stack(np.where(thresh > 0))
                angle = cv2.minAreaRect(coords)[-1]
                if angle < -45:
                    angle = -(90 + angle)
                # otherwise, just take the inverse of the angle to make
                # it positive
                else:
                    angle = -angle

                (h, w) = image.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                

                rotated = cv2.warpAffine(image, M, (w, h),
                    flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
                image = rotated
                #image = cv2.resize(image, (4000, 2000 ), interpolation=cv2.INTER_CUBIC)
                # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

                # contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                # cnt = contours
                # s = 1
                # for c in cnt:
                #     #print(cv2.contourArea(c))
                #     if(cv2.contourArea(c)  > 1000000):
                #         s = s + 1
                #         x,y,w,h = cv2.boundingRect(c)
                #         cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
                # if s > 1:
                #     image = image[y:y+h,x:x+w]

                barcodes = pyzbar.decode(image)

                
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
                    print(ts)
                    lastScan = HoldStatus("").readFile("_lastScan")
                    lastSerialCount = HoldStatus("").readFile("_lastScanCount")
                    if(str(lastScan) == str(json.dumps([ele for ele in reversed(serials)])) and str(lastScan)!=""):
                        s = 1

                    # if(int(lastSerialCount) > int(len(serials))):
                    #     s = 1
                    
                    if s == 0:
                        print(serials)
                        HoldStatus("").writeFile(json.dumps([ele for ele in reversed(serials)]), "_lastScan")
                        HoldStatus("").writeFile(str(len(serials)), "_lastScanCount")
                        serials.append(fillenameImage)
                        cv2.imwrite("static/processingImg/boxER_%s.png" % fillenameImage, image)
                        file1 = open("static/uploads/_serial.txt", "a")
                        file1.write(json.dumps([ele for ele in reversed(serials)])+"\n")
                        file1.close()
                    
                

            # Jaccard_accuracy = intersection over union of the two binary masks

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
    # root = tk.Tk()
    # app = App(root)
    MAINTENANCE_INTERVAL = .1

    
    # root.mainloop()
