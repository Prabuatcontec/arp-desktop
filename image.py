import os, shutil
import sys
import pytesseract
import cv2
import numpy as np
from PIL import Image
from flask import session
import json
import time
from modelunitvalidation import ModelValidation
from filehandling import HoldStatus
from scipy.ndimage import interpolation as inter
import time
from config import Config
import os.path
import requests
import pickle
import glob
import imutils
from pyzbar import pyzbar
import random
import re
from datetime import datetime 
import calendar
from timeit import default_timer as timer


ds_factor = 0.6

os.environ['OMP_THREAD_LIMIT'] = '2'
class ImageProcess(object):
    def __init__(self):
        self.validation = open("static/uploads/_validation.txt", 'r').read()
        self.customer = open("static/uploads/_customer.txt").readline().strip("\n")

    def conStatus(self):
        res1 = requests.get(
            Config.API_MOTOR_URL + 'devices',
            headers={'Content-Type': 'application/json'}
        )
        data = res1.json()
        status = data['devices'][0]['controller response']
        open("static/uploads/_status.txt", "w").write(str(status))

    def readData(self):
        status = open("static/uploads/_status.txt").readline().strip("\n")
        changedTime = os.stat("static/uploads/_status.txt")[-2]
        ts = calendar.timegm(time.gmtime())
        if status== "Success" and (ts - changedTime)>3:
            open("static/uploads/_status.txt", "w").write("")
        if os.path.exists("static/uploads/_serial.txt"):
            os.rename("static/uploads/_serial.txt", "static/uploads/_serial_process.txt")
            with open("static/uploads/_serial_process.txt", 'r') as t:
                
                os.remove("static/uploads/_serial_process.txt")
                for i,line in enumerate(t):
                    line = self.trimValue(line)
                    self.processImage(line)
            return 1

    def trimValue(self, line):
        line = line.replace('"', '')
        line = line.replace('[', '')
        line = line.replace(']', '')
        line = line.split(',')
        return line

    def updateFile(self, value, filename):  
        HoldStatus("").writeFile(value, filename)

    def rotate_bound(self, image, angle):
        return imutils.rotate(image, angle) 

    def Reverse(self, lst):
        return [ele for ele in reversed(lst)]

    def processImage(self, line):
        imName = line[0]
        line.pop(0)
        r = open("static/uploads/_goodDataAvailable.txt", "r")
        r = str(r.read())
        rev = self.Reverse(line)
        if(r.find(str(line)) !=-1 or r.find(str(rev)) != -1):
            return 1
        else:
            if os.path.isfile("static/processingImg/boxER_"+imName+".png"):
                    
                    image = cv2.imread("static/processingImg/boxER_"+imName+".png")
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    ts = calendar.timegm(time.gmtime())
                    print(ts)
                    print("=============================================")
                    text = pytesseract.image_to_string(Image.fromarray(gray),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
                    #print("".join(text.split()).encode('utf8'))
                    validation = self.validation
                    strVal = str(validation)
                    models = json.loads(strVal)
                    angleSame = 0
                    
                    for key, value in models.items():
                        sub_index = str("".join(text.split())).find(key.replace('"', ""))
                        if sub_index >-1:
                            #print(90)
                            text = ""
                            self.processValidation(key, value, line, imName)
                            angleSame = 1
                            break
                    if(angleSame ==0):
                        lo = [180,-5,5,185,175]
                        for x in lo:
                            #print (x)
                            img = self.rotate_bound(image, x)
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                            text = pytesseract.image_to_string(Image.fromarray(gray),lang='eng', config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-')
                            #print("".join(text.split()).encode('utf8'))
                            r = 0
                            for key, value in models.items():
                                sub_index = str("".join(text.split())).find(key.replace('"', ""))
                                if sub_index >-1:
                                    text = ""
                                    line = self.Reverse(line)
                                    self.processValidation(key, value, line, imName)
                                    r = 1
                                    break
                            if r == 1:
                                break
                    

    def processValidation(self, key, value, line, imName):
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
                    open("static/uploads/_goodDataAvailable.txt", "a").write(str(line)+"\n")
                    mdict1 = {"model": str(jsonArray["model"])}
                    dict.update(mdict1)
                    mdict1 = {"customer": str(self.customer)}
                    dict.update(mdict1)
                
                    open("static/uploads/_status.txt", "w").write("Success")
                    file1 = open("static/uploads/_goodData.txt", "a")
                    file1.write("\n")
                    file1.write(str(dict))
                    line = str(dict).replace("'",'"')
                    response = requests.post(Config.DEEPBLU_URL + '/autoreceive/automation', line,
                                        headers={'Content-Type': 'application/json', 
                                        'Authorization': 'Basic QVVUT1JFQ0VJVkU6YXV0b0AxMjM=' }
                                        )
 
    def postToDeepblu(self):
        return 1
        if os.path.exists("static/uploads/_goodData.txt"):
            os.rename("static/uploads/_goodData.txt", "static/uploads/_goodData_process.txt")
            with open("static/uploads/_goodData_process.txt", 'r') as t:
                os.remove("static/uploads/_goodData_process.txt")
                for i,line in enumerate(t):
                    line = line.replace("'",'"')
                    requests.post(Config.DEEPBLU_URL + '/autoreceive/automation', line,
                                    headers={'Content-Type': 'application/json', 
                                    'Authorization': 'Basic QVVUT1JFQ0VJVkU6YXV0b0AxMjM=' }
                                    )