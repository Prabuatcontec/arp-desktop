from timeit import default_timer as timer
from tkinter.constants import HORIZONTAL

import cv2
import numpy as np
import structlog
from pyzbar import pyzbar

import settings
from detection.mser import find_barcodes
from detection.utils import get_dataset, img_concat

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



logger = structlog.get_logger(__name__)



class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        frame_eb_data = tk.Frame(self, width=1000, height=40)
        frame_eb_data.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        # frame_but_right = tk.Frame(self, width=240, height=60)
        # frame_but_right.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        #lab_eb_data = tk.Label(frame_eb_data, background='#DDD4EF', textvariable=controller.page1_label)
        #lab_eb_data.grid(row=0, column=0)
        self.category = tk.StringVar()
        somechoices = []
        for value in Connection().getCustomer():
           somechoices.append(value[2])

        #somechoices = ["1", "2", "C", "D"]
        self.category.set("Pick a category")

        popupMenu = tk.OptionMenu(frame_eb_data, self.category, *somechoices)
        popupMenu.grid(row=3, column=1)
        self.category.trace('w', self.change_dropdown)

        # b_ebdata = tk.Button(frame_but_right, text="Page 2", width=10, height=2, command=lambda: controller.show_frame(PageTwo))
        # b_ebdata.grid(row=0, column=0)
        frame_eb_data = tk.Frame(self, width=1000, height=50)
        frame_eb_data.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
        self.progress = Progressbar(frame_eb_data, orient=HORIZONTAL,length=100,  mode='indeterminate')
    
    def change_dropdown(self,*args):
        print( self.category.get() )
        HoldStatus("").writeFile("\n", "_serial")
        HoldStatus("").writeFile("", "_lastScan")
        HoldStatus("").writeFile("0", "_lastScanCount")
        HoldStatus("").writeFile("2", "_scan")
        HoldStatus("").writeFile("0", "_serialpostCount")
        HoldStatus("").writeFile("", "_goodData")
        HoldStatus("").writeFile("0", "_processing")
        dict = {}
        self.progress.grid(row=1,column=0)
        self.progress.start()
        for value in Connection().getModels(self.category.get()):
           mdict1 = {value[1]:value[2]}
           dict.update(mdict1)
        self.progress.stop()
        self.progress.grid_forget()
        HoldStatus("").writeFile(json.dumps(dict),"_validation")
        threading.Thread(target=self.maintenance, daemon=True).start()
        threading.Thread(target=self.postingData, daemon=True).start()

    def maintenance(self):
        """ Background thread doing various maintenance tasks """
        readText = ImageProcess()
        while True:
            # do things...
            time.sleep(.1)
            readText.readData()
            
            

    def postingData(self):
        """ Background thread doing various maintenance tasks """
        readText = ImageProcess()
        while True:
            # do things...
            time.sleep(.1)
            readText.postToDeepblu()

        


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Added the self.controller so the method below can use it.
        self.controller = controller
        frame_buttons = tk.Frame(self, width=1000, bg="#DDD4EF", colormap="new")
        frame_buttons.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        frame_up_left = tk.Frame(self, width=1000, height=2000, bg="#89E3FA", colormap="new")
        frame_up_left.grid(row=1, column=0, sticky='w', padx=5, pady=5)

        b_data = tk.Label(frame_buttons, text='Example GUI', font='TrebuchetMS 30 bold', background="#DDD4EF")
        b_data.grid(row=0, column=0, padx=13, pady=5, sticky='w')
        b5 = tk.Button(frame_buttons, text='Set Text', command= self.update_p2_label)
        b5.grid(row=0, column=2, padx=5, pady=5, sticky='e')
        b6 = tk.Button(frame_buttons, text='Page 1', command=lambda: controller.show_frame(PageOne))
        b6.grid(row=0, column=3, padx=5, pady=5, sticky='e')

        self.entry_nombre_fld = tk.Entry(frame_up_left, width=1000)
        self.entry_nombre_fld.grid(row=1, column=1, columnspan=3, sticky='w')
        label_2 = tk.Label(frame_up_left, text="Name:", font=("bold", 14))
        label_2.grid(row=1, column=0, sticky='e')

       

        frame_video = tk.Frame(self, width=1000, height=2000, bg="#DDD4EF", colormap="new")
        frame_video.grid(row=0, column=4, padx=50, pady=50, sticky='e')
        
        self.stopEvent = None
        self.frame = frame_video
        tk.Label(self.frame, text='Page 1').pack()
        
        self.vs = VideoStream(0).start()
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        self.panel = None

        

    

    # # Added this function to update the page1_label StringVar.
    def update_p2_label(self):
        self.controller.page1_label.set(self.entry_nombre_fld.get())

    def videoLoop(self):
        stats = []
        start = timer()
		# DISCLAIMER:
		# I'm not a GUI developer, nor do I even pretend to be. This
		# try/except statement is a pretty ugly hack to get around
		# a RunTime error that Tkinter throws due to threading
        # keep looping over frames until we are instructed to stop
        while not self.stopEvent.is_set():
            # grab the frame from the video stream and resize it to
            # have a maximum width of 300 pixels
            self.frame = self.vs.read()
            #self.frame = cv2.imread("sddddd.png")
            self.frame = imutils.resize(self.frame, width=1000, height=1500)
    
            # OpenCV represents images in BGR order; however PIL
            # represents images in RGB order, so we need to swap
            # the channels, then convert to PIL and ImageTk format
            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
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
                #image = cv2.resize(image, (4000, 2000 ), interpolation=cv2.INTER_CUBIC)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

                _, contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                cnt = contours
                s = 1
                for c in cnt:
                    if(cv2.contourArea(c)  > 1000000):
                        s = s + 1
                        x,y,w,h = cv2.boundingRect(c)
                        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
                if s > 1:
                    image = image[y:y+h,x:x+w]
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
                    lastScan = HoldStatus("").readFile("_lastScan")
                    lastSerialCount = HoldStatus("").readFile("_lastScanCount")
                    
                    if(str(lastScan) == str(json.dumps([ele for ele in reversed(serials)])) and str(lastScan)!=""):
                        s = 1
                    # if(int(lastSerialCount) > int(len(serials))):
                    #     s = 2
                    
                    if s == 0:
                        print(serials)
                        HoldStatus("").writeFile(json.dumps([ele for ele in reversed(serials)]), "_lastScan")
                        HoldStatus("").writeFile(str(len(serials)), "_lastScanCount")
                        serials.append(fillenameImage)
                        cv2.imwrite("static/processingImg/boxER_%s.jpg" % fillenameImage, image)
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
        self.page2_entry = tk.StringVar()

        
        

        container = tk.Frame(self)
        container.pack(side='top')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (PageOne, PageTwo):
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
