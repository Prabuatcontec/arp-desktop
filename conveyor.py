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
            res1 = requests.post(
                Config.API_MOTOR_URL + 'devices/2', data=json.dumps({"state": "ON"}),
                headers={'Content-Type': 'application/json'}
            )
            res1 = requests.post(
                Config.API_MOTOR_URL + 'devices/2', data=json.dumps({ "spd": "HIGH"}),
                headers={'Content-Type': 'application/json'}
            )
            res1 = requests.post(
                Config.API_MOTOR_URL + 'devices/3', data=json.dumps({"state": "ON"}),
                headers={'Content-Type': 'application/json'}
            )
    
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
        res1 = requests.post(
            Config.API_MOTOR_URL + 'devices/3', data=json.dumps({"state": "ON"}),
            headers={'Content-Type': 'application/json'}
        )
        res1 = requests.post(
            Config.API_MOTOR_URL + 'devices/1', data=json.dumps({"state": "ON"}),
            headers={'Content-Type': 'application/json'}
        )
        res1 = requests.post(
            Config.API_MOTOR_URL + 'devices/1', data=json.dumps({ "spd": "HIGH"}),
            headers={'Content-Type': 'application/json'}
        )
        return 1

    def closeConveyor(self):
        requests.post(
            Config.API_MOTOR_URL + 'devices/1', data=json.dumps({"state": "OFF"}),
            headers={'Content-Type': 'application/json'}
        )
        requests.post(
            Config.API_MOTOR_URL + 'devices/3', data=json.dumps({"state": "OFF"}),
            headers={'Content-Type': 'application/json'}
        )
        return 1

    def enableLight(self, state):
        res1 = requests.post(
            Config.API_MOTOR_URL + 'devices/4', data=json.dumps({"state": state}),
            headers={'Content-Type': 'application/json'}
        )

    def resetLastScan(key, value):
        calib_result_pickle = {}
        calib_result_pickle["key"] = key
        calib_result_pickle["value"] = value
        pickle.dump(calib_result_pickle, open(get_correct_path("static/uploads/lastScan.p"), "wb" )) 

        
def get_correct_path(relative_path):
    p = os.path.abspath(".").replace('/dist', "")
    return os.path.join(p, relative_path)