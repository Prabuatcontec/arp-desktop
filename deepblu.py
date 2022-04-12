import os
import json
from config import Config
import os.path
import requests
from datetime import datetime 
import socket
class Deepblu(object):

    def getPalletId(self,model):
        user = open(get_correct_path("static/uploads/_login.txt")).readline().strip("\n")
        response = requests.get(Config.DEEPBLU_URL + '/autoreceive/pallet/latest?model='+model+'&stationId='+Config.STATION_ID+'&addUser='+user,
                                            headers={'Content-Type': 'application/json', 
                                            'Authorization': 'Basic QVVUT1JFQ0VJVkU6YXV0b0AxMjM=' }, verify=False
                                            )
        return response
    
    def closePallet(self):
        response = requests.patch(Config.DEEPBLU_URL + '/autoreceive/closepallet',  data=json.dumps({"palletId": open(get_correct_path("static/uploads/_palletId.txt")).readline().strip("\n")}),
                                        headers={'Content-Type': 'application/json', 
                                        'Authorization': 'Basic QVVUT1JFQ0VJVkU6YXV0b0AxMjM=' }, verify=False
                                )
        return response

    def printPalletTag(self, palletDetail):
        palletID = palletDetail[0]['palletId']
        itemID = palletDetail[0]['itemId']
        itemName = palletDetail[0]['itemName']
        model = palletDetail[0]['model']
        cusItemID = palletDetail[0]['cusItemId']
        qty = str(palletDetail[0]['qty'])
        warehouse = str(datetime.today().strftime('%m%d%y'))+palletDetail[0]['warehouseCode']
        palletTag = "^XA^MMT^PW812^LL0406^LS0^FT288,38^A0N,31,38^FH\^FDPALLET ID TAG^FS^BY3,3,81^FT23,131^BCN,,N,N^FD>:"+palletID+"^FS^FT64,205^A0N,70,69^FH\^FD"+palletID+"^FS^FT324,253^A0N,31,31^FH\^FD"+itemID+"^FS^FT23,307^A0N,31,31^FH\^FD"+itemName+"^FS^FT23,348^A0N,31,31^FH\^FD"+model+"^FS^FT21,391^A0N,31,31^FH\^FDOrig Qty:^FS^FT136,391^A0N,31,31^FH\^FD"+qty+"^FS^FT550,349^A0N,25,24^FH\^FD"+cusItemID+"^FS^FT664,391^A0N,31,31^FH\^FD"+warehouse+"^FS^PQ1,0,1,Y^XZ"
        print(palletTag)
        mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)         
        host = Config.PRINTER_IP
        port = 9100   
        try:           
            mysocket.connect((host, port)) #connecting to host
            mysocket.send(palletTag.encode('ascii'))#using bytes
            mysocket.send(palletTag.encode('ascii'))#using bytes
            mysocket.close () #closing connection
            print("Label")
        except:
            print("Error with the connection")

    def postScannedSerial(self, line):
        response = requests.post(Config.DEEPBLU_URL + '/autoreceive/automationdata', line,
                                            headers={'Content-Type': 'application/json', 
                                            'Authorization': 'Basic QVVUT1JFQ0VJVkU6YXV0b0AxMjM=' }, verify=False
                                            )
        return response

        
def get_correct_path(relative_path):
    p = os.path.abspath(".").replace('/dist', "")
    return os.path.join(p, relative_path)