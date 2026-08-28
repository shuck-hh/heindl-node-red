#!/usr/bin/env python3
########################################################################
# Filename    : I2CLCD1602.py
# Description : Use the LCD display data
# Author      : freenove; modified to fit project usecase by: shuck 
# modification: 2023/05/15
########################################################################
import os
import smbus
import time
from time import sleep
from datetime import datetime
from LCD1602 import CharLCD1602

lcd1602 = CharLCD1602()   

def get_cpu_temp():     # get CPU temperature from file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C '
 
def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')
    
def loop():
    lcd1602.init_lcd()
    count = 0
    while(True):
        # lcd1602.clear()
        lcd1602.write(0, 0, "Hallo")# display CPU temperature
        lcd1602.write(0, 1, get_time_now() )   # display the time
        sleep(1)
def destroy():
    lcd1602.clear()

def überwache_datei(dateipfad, intervall=1):
    try:
        letzter_status = os.path.getmtime(dateipfad)
    except FileNotFoundError:
        print("Datei nicht gefunden!")
        return

    print(f"Überwachung gestartet für: {dateipfad}")

    while True:
        try:
            aktueller_status = os.path.getmtime(dateipfad)
            
            if aktueller_status != letzter_status:
                print("Datei wurde geändert!")
                letzter_status = aktueller_status

        except FileNotFoundError:
            print("Datei wurde gelöscht oder ist nicht erreichbar!")

        time.sleep(intervall)

if __name__ == '__main__':
    print ('Program is starting ... ')
    überwache_datei("../cpp/keys.txt", intervall=2)
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

