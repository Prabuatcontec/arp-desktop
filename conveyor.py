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
class Conveyor(object):

    def callAllConveyor(self):
        customer = open("static/uploads/_customer.txt").readline().strip("\n")
        if(customer != ""):
            res1 = requests.post(
                Config.API_MOTOR_URL + 'devices/1', data=json.dumps({"state": "ON"}),
                headers={'Content-Type': 'application/json'}
            )
            res1 = requests.post(
                Config.API_MOTOR_URL + 'devices/1', data=json.dumps({ "spd": "HIGH"}),
                headers={'Content-Type': 'application/json'}
            )
            print('call 1')
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
    
    def CloseAllConveyor(self):
        requests.post(
            Config.API_MOTOR_URL + 'devices/1', data=json.dumps({"state": "OFF"}),
            headers={'Content-Type': 'application/json'}
        )
        requests.post(
            Config.API_MOTOR_URL + 'devices/3', data=json.dumps({"state": "OFF"}),
            headers={'Content-Type': 'application/json'}
        )
        requests.post(
            Config.API_MOTOR_URL + 'devices/2', data=json.dumps({"state": "OFF"}),
            headers={'Content-Type': 'application/json'}
        )

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