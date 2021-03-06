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
import glob
import pickle


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

    def change_dropdown(self,*args):
        open("static/uploads/_customer.txt", "w").write(f"{self.category.get() }")
        #HoldStatus("").writeFile("", "_goodData")
        #open("static/uploads/_serial.txt", "w").write("")
        open("static/uploads/_status.txt", "w").write("")
        open("static/uploads/_lastFail.txt", "w").write("")
        #open("static/uploads/_lastScan.txt", "w").write("")
        open("static/uploads/_goodDataAvailable.txt", "w").write("")
        open("static/uploads/_serialUpdate.txt", "w").write("")
        
        
        
        
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
        
        res1 = requests.post(
            Config.API_MOTOR_URL + 'devices/1', data=json.dumps({"state": "ON"}),
            headers={'Content-Type': 'application/json'}
        )
        res1 = requests.post(
            Config.API_MOTOR_URL + 'devices/1', data=json.dumps({ "spd": "HIGH"}),
            headers={'Content-Type': 'application/json'}
        )
        print(res1)
        res1 = requests.post(
            Config.API_MOTOR_URL + 'devices/2', data=json.dumps({"state": "ON"}),
            headers={'Content-Type': 'application/json'}
        )
        res1 = requests.post(
            Config.API_MOTOR_URL + 'devices/2', data=json.dumps({ "spd": "HIGH"}),
            headers={'Content-Type': 'application/json'}
        )
        print(res1)
        res1 = requests.post(
            Config.API_MOTOR_URL + 'devices/3', data=json.dumps({"state": "ON"}),
            headers={'Content-Type': 'application/json'}
        )
        print(res1)
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

        
        b5 = tk.Button(frame_buttons, text='Take Pic', command= self.update_p2_label)
        b5.grid(row=0, column=0, padx=1, pady=1, sticky='w')
        b6 = tk.Button(frame_buttons, text='Calibrate', command=self.calibrateIt)
        b6.grid(row=0, column=1, padx=1, pady=1, sticky='w')

        # self.entry_nombre_fld = tk.Entry(frame_up_left, width=25)
        # self.entry_nombre_fld.grid(row=0, column=1, sticky='w')
        # self.entry_nombre_fld1 = tk.Entry(frame_up_left1, width=25,  show='*')
        # self.entry_nombre_fld1.grid(row=0, column=1, sticky='w')
        # label_2 = tk.Label(frame_up_left, text="Username:", font=("bold", 14))
        # label_2.grid(row=0, column=0, sticky='w')
        # label_21 = tk.Label(frame_up_left1, text="Password: ", font=("bold", 14))
        # label_21.grid(row=0, column=0, sticky='w')
        lab_eb_data = tk.Label(frame_buttons, textvariable=self.controller.page2_label)
        lab_eb_data.grid(row=3, column=0, columnspan=2)

       
        
        frame_video = tk.Frame(self, width=1400, height=1800, colormap="new")
        frame_video.grid(row=3, column=0, padx=1, pady=1, sticky='e')
        
        self.stopEvent = None
        self.frame = frame_video

        tk.Label(self.frame, text='').pack()

        open("static/uploads/_cap.txt", "w").write("0")
        open("static/uploads/_ready.txt", "w").write("0")
        #self.vs = VideoStream(0)
        self.vs  = cv2.VideoCapture(4)
        self.vs .set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
        self.vs .set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
        self.vs.set(cv2.CAP_PROP_AUTOFOCUS, 0)        
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        self.panel = None


    # # Added this function to update the page1_label StringVar.
    def update_p2_label(self):
        open("static/uploads/_cap.txt", "w").write("1")
        return 1
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

    
    def calibrateIt(self):
 
        # Chessboard dimensions
        number_of_squares_X = 10 # Number of chessboard squares along the x-axis
        number_of_squares_Y = 7  # Number of chessboard squares along the y-axis
        nX = number_of_squares_X - 1 # Number of interior corners along x-axis
        nY = number_of_squares_Y - 1 # Number of interior corners along y-axis
        

        # Store vectors of 3D points for all chessboard images (world coordinate frame)
        object_points = []
        
        # Store vectors of 2D points for all chessboard images (camera coordinate frame)
        image_points = []
        
        # Set termination criteria. We stop either when an accuracy is reached or when
        # we have finished a certain number of iterations.
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        
        # Define real world coordinates for points in the 3D coordinate frame
        # Object points are (0,0,0), (1,0,0), (2,0,0) ...., (5,8,0)
        object_points_3D = np.zeros((nX * nY, 3), np.float32)       
        
        # These are the x and y coordinates                                              
        object_points_3D[:,:2] = np.mgrid[0:nY, 0:nX].T.reshape(-1, 2) 
        print(3339999999999999)
        images = glob.glob('static/calibration/*.png')
        
        for image_file in images:
            image = cv2.imread(image_file)

        #image = self.Zoom(image,2)
        img1 = image
        #image = cv2.imread('1622798624-214896_undistorted.jpg')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, jpeg = cv2.imencode('.png', image)

        # Find the corners on the chessboard
        success, corners = cv2.findChessboardCorners(gray, (nY, nX), None)
        
        images = glob.glob('static/calibration/*.png')

        print(9999999999999)    
          # Go through each chessboard image, one by one
        for image_file in images:
            print(image_file)
        
            # Load the image
            image = cv2.imread(image_file)  
        
            # Convert the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
        
            # Find the corners on the chessboard
            success, corners = cv2.findChessboardCorners(gray, (nY, nX), None)
            
            # If the corners are found by the algorithm, draw them
            if success == True:
        
            # Append object points
                object_points.append(object_points_3D)
            
                # Find more exact corner pixels       
                corners_2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)       
                
                        # Append image points
                image_points.append(corners)
            
                # Draw the corners
                cv2.drawChessboardCorners(image, (nY, nX), corners_2, success)
        
            # Display the image. Used for testing.
            #cv2.imshow("Image", image) 
            
            # Display the window for a short period. Used for testing.
            #cv2.waitKey(200) 

        distorted_image = image
        # len(cv2.calibrateCamera(object_points, 
        #                                                     image_points, 
        #                                                     gray.shape[::-1], 
        #                                                     None, 
        #                                                     None))
        # Perform camera calibration to return the camera matrix, distortion coefficients, rotation and translation vectors etc 
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, 
                                                            image_points, 
                                                            gray.shape[::-1], 
                                                            None, 
                                                            None)
        
        # Get the dimensions of the image 
        height, width = distorted_image.shape[:2]
            
        # Refine camera matrix
        # Returns optimal camera matrix and a rectangular region of interest
        optimal_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, 
                                                                    (width,height), 
                                                                    1, 
                                                                    (width,height))
        
        # Undistort the image 
        

        # Create the output file name by removing the '.jpg' part
        

        calib_result_pickle = {}
        calib_result_pickle["mtx"] = mtx
        calib_result_pickle["optimal_camera_matrix"] = optimal_camera_matrix
        calib_result_pickle["dist"] = dist
        calib_result_pickle["rvecs"] = rvecs
        calib_result_pickle["tvecs"] = tvecs
        pickle.dump(calib_result_pickle, open("static/uploads/camera_calib_pickle.p", "wb" )) 

        return calib_result_pickle
    
    def get_correct_path(relative_path):
        p = os.path.abspath(".").replace('/dist', "")
        return os.path.join(p, relative_path)

    def videoLoop(self):
        stats = []
        start = timer()
        while not self.stopEvent.is_set():
            flag,self.frame = self.vs.read()
            if flag is None:
                print ("Failed")
            customer = open("static/uploads/_customer.txt").readline().strip("\n")
            #status = open("static/uploads/_status.txt").readline().strip("\n")
            
            #customer = 1
            if open("static/uploads/_cap.txt").readline().strip("\n") == "1" or open("static/uploads/_ready.txt").readline().strip("\n") == "1":
                print("cap")
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                # calib_result_pickle = pickle.load(open("static/uploads/camera_calib_pickle.p", "rb" ))
                # mtx = calib_result_pickle["mtx"]
                # optimal_camera_matrix = calib_result_pickle["optimal_camera_matrix"]
                # dist = calib_result_pickle["dist"]
                # image = cv2.undistort(image, mtx, dist, None, 
                #             optimal_camera_matrix)
                # if status == "Success":
                #     cv2.putText(image, "Status:"+status, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 100, 0), 8)
                # elif status == "":
                #     cv2.putText(image, "Status:Waiting", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 150, 0), 8)
                # else:
                #     cv2.putText(image, "Status:Failed", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 8)
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
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                #image1 = image

            
                 
                 
       
            #open(get_correct_path("static/uploads/_cap.txt"), "w").write("1")
            if open("static/uploads/_cap.txt").readline().strip("\n") == "1":
                print("Capme")
                gmt = time.gmtime()
                ts = calendar.timegm(gmt)
                fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
                cv2.imwrite("static/calibration/Goos_boxER_"+fillenameImage+".png", image)
                open("static/uploads/_ready.txt", "w").write("1")
                open("static/uploads/_cap.txt", "w").write("0")

            #return 1
                
                # s = 2
                # if open("static/uploads/_serialUpdate.txt").readline().strip("\n") == "1":
                #     s = 1
                #     print('val=1')
                # if (s > 1):
                    
                #     open("static/uploads/_serialUpdate.txt", "w").write("1")
                #     lo = [0, -5, 5, -10, 10]
                #     for x in lo:
                #         if (x != 0):
                #             image1 = self.rotate_bound(image, x)
                #         barcodes = pyzbar.decode(image1)
                #         if len(barcodes) > 1:
                #             gmt = time.gmtime()
                #             ts = calendar.timegm(gmt)
                #             fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
                            
                #             #HoldStatus("").writeFile(json.dumps([ele for ele in reversed(serials)]), "_lastScan")
                #             cv2.imwrite("static/processingImg/Goos_boxER_%s.png" % fillenameImage, image)
                #             image = image1
                #             break
                #     serials = []
                #     for barcode in barcodes:
                #         barcodeData = barcode.data.decode("utf-8")
                #         if(detect_special_characer(barcodeData) == True):
                #             serials.append(barcodeData)

                #     r = open("static/uploads/_goodDataAvailable.txt", "r")
                #     r = str(r.read())
                #     rev = self.Reverse(serials)
                #     if(r.find(str(serials)) !=-1 or r.find(str(rev)) != -1):
                #         open("static/uploads/_serialUpdate.txt", "w").write("0")
                #         print('goodSerial=1')
                #     else:
                #         sr = 0
                #         if len(serials) > 1:
                            
                #             start = time.time()
                #             print(start)
                #             if sr == 0:
                #                 thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                #                 contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                #                 cnt = contours
                #                 s = 1
                #                 for c in cnt:
                #                     #print(cv2.contourArea(c))
                #                     if(cv2.contourArea(c)  > 100000):
                #                         s = s + 1
                #                         x,y,w,h = cv2.boundingRect(c)
                #                 print(serials)
                #                 print(s)
                #                 if s > 1:
                #                     gmt = time.gmtime()
                #                     ts = calendar.timegm(gmt)
                #                     fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
                #                     image = thresh[y:y+h,x:x+w]
                #                     #HoldStatus("").writeFile(json.dumps([ele for ele in reversed(serials)]), "_lastScan")
                #                     cv2.imwrite("static/processingImg/boxER_%s.png" % fillenameImage, image)
                #                     self.processImage(serials, image, image)
                #                 else:
                #                     open("static/uploads/_serialUpdate.txt", "w").write("0")
                                    
                #             # serials.append(fillenameImage)
                #             # cv2.imwrite("static/processingImg/boxER_%s.png" % fillenameImage, image)
                #             # file1 = open("static/uploads/_serial.txt", "a")
                #             # file1.write(json.dumps([ele for ele in reversed(serials)])+"\n")
                #             # file1.close()

                #         else:
                #             open("static/uploads/_serialUpdate.txt", "w").write("0")


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
            print("".join(text.split()).encode('utf8'))
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
                
            if r == 0:
                self.closeConveyor()
                str1 = " " 
                if str(str1.join(line)) != open("static/uploads/_lastFail.txt").readline().strip("\n"):
                    self.enableLight("RED")
                    tkinter.messagebox.askretrycancel("Unit OCR Failed", "For Units:"+ str1.join(line)+". Try to position the box in 0 or 180 degree and click retry. ")
                    open("static/uploads/_lastFail.txt", "w").write(str(str1.join(line)))
                    self.enableLight("OFF")

                self.callConveyor()
                open("static/uploads/_serialUpdate.txt", "w").write("0")

    def gradiant(self,p1,p2):
        return (p1[1]-p2[1])/(p2[0]-p1[0])
    
    def getAngel(self):
        if(len(self.p)>=3):
            p1,p2,p3 =self.p[-3:]
            m1 = self.gradiant(p1,p2)
            m2 = self.gradiant(p1,p3)
            aR = math.atan((m2-m1)/(1+(m2*m1)))
            aD = round(math.degrees(aR))
            print(aD)

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
                self.closeConveyor()
                str1 = " " 
                if str(str1.join(line)) != open("static/uploads/_lastFail.txt").readline().strip("\n"):
                    self.enableLight("RED")
                    tkinter.messagebox.askretrycancel("Unit Validation Failed", "Serials:"+ str1.join(line))
                    open("static/uploads/_lastFail.txt", "w").write(str(str1.join(line)))
                    self.enableLight("OFF")
                self.callConveyor()
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
                    #gmt = time.gmtime()
                    #ts = calendar.timegm(gmt)
                    customer = open("static/uploads/_customer.txt").readline().strip("\n")
                    #gmt = time.gmtime()
                    #ts = calendar.timegm(gmt)
                    #fillenameImage = str(str(ts)+'-'+str(random.randint(100000,999999)))
                    open("static/uploads/_goodDataAvailable.txt", "a").write(str(line)+"\n")
                    #cv2.imwrite("static/processingImg/boxER_%s.png" % str(random.randint(100000,999999)), image)
                    
                    mdict1 = {"model": str(jsonArray["model"])}
                    dict.update(mdict1)
                    mdict1 = {"customer": str(customer)}
                    dict.update(mdict1)
                
                    # open("static/uploads/_status.txt", "w").write("Success")
                    # file1 = open("static/uploads/_goodData.txt", "a")
                    # file1.write("\n")
                    # file1.write(str(dict))
                    line = str(dict).replace("'",'"')
                    requests.post(Config.DEEPBLU_URL + '/autoreceive/automation', line,
                                        headers={'Content-Type': 'application/json', 
                                        'Authorization': 'Basic QVVUT1JFQ0VJVkU6YXV0b0AxMjM=' }
                                        )
                    print('success')
                    self.enableLight("GREEN")
                    open("static/uploads/_serialUpdate.txt", "w").write("0")
                    self.callConveyor()
                    start = time.time()
                    print(start)
            
    def enableLight(self, state):
        # print("Light On")
        # readStatus = ImageProcess()
        # status = readStatus.getConState("4")
        
        # if (status=="OFF"):
        res1 = requests.post(
            Config.API_MOTOR_URL + 'devices/4', data=json.dumps({"state": state}),
            headers={'Content-Type': 'application/json'}
        )
        print(res1)

    
    def callConveyor(self):
        print("start conv")
        start = time.time()
        print(start)
        res1 = requests.post(
            Config.API_MOTOR_URL + 'devices/3', data=json.dumps({"state": "ON"}),
            headers={'Content-Type': 'application/json'}
        )
        print(res1)
        res1 = requests.post(
            Config.API_MOTOR_URL + 'devices/1', data=json.dumps({"state": "ON"}),
            headers={'Content-Type': 'application/json'}
        )
        print(res1)
        res1 = requests.post(
            Config.API_MOTOR_URL + 'devices/1', data=json.dumps({ "spd": "HIGH"}),
            headers={'Content-Type': 'application/json'}
        )
        print(res1)
        start = time.time()
        print(start)
        return 1

    def closeConveyor(self):
        print("stop conv")
        start = time.time()
        requests.post(
            Config.API_MOTOR_URL + 'devices/1', data=json.dumps({"state": "OFF"}),
            headers={'Content-Type': 'application/json'}
        )
        requests.post(
            Config.API_MOTOR_URL + 'devices/3', data=json.dumps({"state": "OFF"}),
            headers={'Content-Type': 'application/json'}
        )
        print(start)
        return 1


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

