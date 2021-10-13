# ARP Desktop


pyinstaller --onefile --icon="logo1.ico" --hidden-import pandas._libs.tslibs.base --hidden-import PIL._tkinter_finder --name="ARP" -i "logo1.ico" arp_change.py
