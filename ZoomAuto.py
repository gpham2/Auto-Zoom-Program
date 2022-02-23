import pyautogui
import datetime
import time as t
import cv2
import os
import webbrowser
import pygetwindow
import numpy
import pytesseract
import pandas as pd

class ZoomObject:
    
    def __init__(self, linkOrID, passw, jTime, lTime, autoleave, nickName):
        self.linkOrID = linkOrID
        self.passw = passw
        self.jTime = jTime
        self.lTime = lTime
        self.autoleave = autoleave
        self.nickName = nickName
        self.active = True
        
    def zoomStart(self):
        success = False
        os.system("taskkill /im Zoom.exe")
        clickBtn("C:\\Users\\giang\\zoom_auto2\\references\\leave.png", 3)
        t.sleep(2)
        if ("zoom.us") in self.linkOrID:
            webbrowser.open_new(self.linkOrID)
            if (len(self.passw) > 0):
                found = findImage("C:\\Users\\giang\\zoom_auto2\\references\\join_meeting_greyed.png", 15)
                if (found != None):
                    pyautogui.write(self.passw)
                    pyautogui.press('enter')
            found = findImage('C:\\Users\\giang\\zoom_auto2\\references\\join_no_vid.png', 60)
            if (found != None):
                pyautogui.moveTo(found)
                pyautogui.click()
                success = True
            else:
                quit()
        else:
            with pyautogui.hold('win'):
               pyautogui.press(['m'])
            os.startfile("C:\\Users\\giang\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe")
            findImage('C:\\Users\\giang\\zoom_auto2\\references\\zoom_app.png', 15)
            clickBtn('C:\\Users\\giang\\zoom_auto2\\references\\join_meeting.png', 15)
            found = findImage('C:\\Users\\giang\\zoom_auto2\\references\\meeting_id.png', 15)
            if (found != None):
                pyautogui.moveTo(found)
                pyautogui.click()
                pyautogui.write(self.linkOrID)
            else:
                quit()
            sec = 0
            while True:
                check_btn = pyautogui.locateAllOnScreen('C:\\Users\\giang\\zoom_auto2\\references\\check_btn.png', confidence = .8)
                if (check_btn != None):
                    for btn in check_btn:
                        pyautogui.moveTo(btn)
                        pyautogui.click()
                        t.sleep(.005)
                    break
                elif (sec > 15):
                    quit()
                    break
                sec = sec + 1
                time.sleep(1)
            found = findImage('C:\\Users\\giang\\zoom_auto2\\references\\join_btn.png', 15)
            if (found != None):
                pyautogui.moveTo(found)
                pyautogui.click()
                success = True
            else:
                quit()
            found = findImage('C:\\Users\\giang\\zoom_auto2\\references\\password.png', 15)
            if (found != None):
                pyautogui.moveTo(found)
                pyautogui.click()
                pyautogui.write(self.passw)
                pyautogui.press('enter')
        t.sleep(4)
        if (self.autoleave and success):
            sec = 0
            while True:
                waiting_room = pyautogui.locateCenterOnScreen('C:\\Users\\giang\\zoom_auto2\\references\\waiting_room.png', confidence = .8)
                if(waiting_room == None):
                    break
                elif (sec > 200):
                    break
                sec = sec + 1
                t.sleep(1.5)
            t.sleep(3)
            win = pygetwindow.getWindowsWithTitle('Zoom')[0]
            win.activate()
            with pyautogui.hold('alt'):
                pyautogui.press(['u'])
    def zoomEnd(self):
        endTime = datetime.datetime.strptime(self.lTime, '%H:%M')
        if (self.autoleave):
            maxNum = 1  
        while True:
            currTime = datetime.datetime.now()
            now = datetime.datetime.now().strftime("%H:%M")
            if (currTime.hour == endTime.hour) and (currTime.minute == endTime.minute):
                   break
            setting = True
            df = pd.read_csv("C:\\Users\\giang\\zoom_auto2\\references\\record.csv")
            if (setting and now in str(df['jTime'])):
                row = df.loc[df['jTime'] == now]
                if str(row.iloc[0,2]) != self.jTime:
                    break
            if (self.autoleave): 
                threshold = maxNum * .25
                part = pyautogui.locateOnScreen('C:\\Users\\giang\\zoom_auto2\\references\\participant.png', confidence = .8)
                if (part != None):
                    im = pyautogui.screenshot(region=(part[0], part[1], part[2] + 50, part[3]))
                    image = numpy.array(im)
                    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    options = "outputbase digits"
                    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                    text = pytesseract.image_to_string(rgb, config=options)
                    num = int(text)
                    if (num > maxNum):
                        maxNum = num
                    elif (num <= threshold):
                        break
            t.sleep(40)
        os.system("taskkill /im Zoom.exe")
        clickBtn('C:\\Users\\giang\\zoom_auto2\\references\\leave.png', 15)
    def startAndEnd(self):
        self.zoomStart()
        self.zoomEnd()
def clickBtn(image, maxSec):
    sec = 0
    while True:
        btn = pyautogui.locateCenterOnScreen(image, confidence = .8)
        if (btn != None):
            pyautogui.moveTo(btn)
            pyautogui.click()
            break
        elif (sec > maxSec):
            break
        sec = sec + 1
        t.sleep(1)
def findImage(image, maxSec):
    sec = 0
    while True:
        imageArea = pyautogui.locateCenterOnScreen(image, confidence = .8)
        if (imageArea != None):
            break
        elif (sec > maxSec):
            break
        sec = sec + 1
        t.sleep(1)
    return imageArea
while True:
    df = pd.read_csv("C:\\Users\\giang\\zoom_auto2\\references\\record.csv")
    now = datetime.datetime.now().strftime("%H:%M")
    if now in str(df['jTime']):
        row = df.loc[df['jTime'] == now]
        linkOrID = str(row.iloc[0,0])
        if str(row.iloc[0,1]) == "nan":
            passw = ""
        else:
            passw = str(row.iloc[0,1])
        jTime = str(row.iloc[0,2])
        lTime = str(row.iloc[0,3])
        if str(row.iloc[0,4]) == "True":
            autoleave = True
        else:
            autoleave = False
        nickName = str(row.iloc[0,5])
        zoomInstance = ZoomObject(linkOrID, passw, jTime, lTime, autoleave, nickName)
        zoomInstance.startAndEnd()
    else:
        t.sleep(40)

