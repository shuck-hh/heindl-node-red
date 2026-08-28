#!/usr/bin/env python3
import os
import smbus
import time
from time import sleep
from datetime import datetime
from LCD1602 import CharLCD1602

lcd1602 = CharLCD1602()   

content = ""
selectedLine = None
input_active = False  # NEU: merkt ob wir gerade schreiben
contentLine1 = "MIN: "
contentLine2 = "MAX: "

def loop(dateipfad):
    global content, selectedLine, input_active, contentLine1, contentLine2

    lcd1602.init_lcd()
    lcd1602.write(0, 0, "MIN: ")
    lcd1602.write(0, 1, "MAX: ")

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
                letzter_status = aktueller_status

                with open(dateipfad, "r") as f:
                    content = f.read().rstrip("\n")

                print("Neuer Inhalt:", content)

                # Steuerlogik
                if content == "A":
                    selectedLine = 0
                    input_active = True
                    if contentLine1 == None:
                        print("Schreibe in Zeile 1")
                        lcd1602.openlight()
                        time.sleep(0.005)
                    else:
                        contentLine1 = None
                        print("Schreibe in Zeile 1")
                        lcd1602.openlight()
                        time.sleep(0.005)

                elif content == "B":
                    selectedLine = 1
                    input_active = True
                    if contentLine2 == None:
                        print("Schreibe in Zeile 2")
                        lcd1602.openlight()
                        time.sleep(0.005)
                    else:
                        contentLine2 = None
                        print("Schreibe in Zeile 2")
                        lcd1602.openlight()
                        time.sleep(0.005)

                elif content == "D":
                    finishInput()

                else:
                    # Nur schreiben wenn aktiv
                    if input_active:
                        startInput(content)

        except FileNotFoundError:
            print("Datei wurde gelöscht oder ist nicht erreichbar!")

        time.sleep(0.2)


def startInput(text):
    global selectedLine, contentLine1, contentLine2

    if selectedLine == 0:
        if contentLine1 == None:
            lcd1602.write(0, 0, "MIN: " + text.ljust(10))
            contentLine1 = text
        else:
            contentLine1 = contentLine1 + text
            lcd1602.write(0, 0, "MIN: " + contentLine1.ljust(10))
    elif selectedLine == 1:
        if contentLine2 == None:
            lcd1602.write(0, 1, "MAX: " + text.ljust(10))
            contentLine2 = text
        else:
            contentLine2 = contentLine2 + text
            lcd1602.write(0, 1, "MAX: " + contentLine2.ljust(10))


def finishInput():
    global input_active, selectedLine, contentLine1, contentLine2

    print("Eingabe beendet")
    lcd1602.write(0, 0, "Wird gespeichert...")
    time.sleep(2)
    lcd1602.clear()
    print("contentLine1: "+ contentLine1)
    lcd1602.write(0, 0, "MIN: " + contentLine1 + "*C")
    print("contentLine2: "+ contentLine2)
    lcd1602.write(0, 1, "MAX: " + contentLine2 + "*C")
    input_active = False
    if selectedLine == 0:
        # write (overwrite) the file
        with open("min.txt", "w", encoding="utf-8") as f:
            f.write(contentLine1)
            print("MIN value in min.txt geschrieben")
    elif selectedLine == 1:
        with open("max.txt", "w", encoding="utf-8") as f:
            f.write(contentLine2)
            print("MAX value in max.txt geschrieben")
    else:
        print("Invalid Line")
    selectedLine = None
    time.sleep(2)
    lcd1602.closelight()




def destroy():
    lcd1602.clear()


if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        loop("keys.txt")
    except KeyboardInterrupt:
        destroy()