import numpy as np
from PIL import ImageGrab, Image
import cv2
import pytesseract
import math
import requests
import json
import time
import pyautogui, sys
import re
import base64
import random

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

config = json.loads(open(r'C:\Users\ssury\Desktop\talku\config.json').read())

oldtxt = 'asdasfasfa'

class Imaging:
    def insert_equal(self, string, index):
        return string[:index] + '=' + string[index:]
    
    def process(self, greyImg):
        custom_config = r' --oem 3 --psm 6'
        txt = pytesseract.image_to_string(greyImg, config= custom_config)
        print('Start: ' + txt)
        global oldtxt
        if txt == oldtxt:
            oldtxt = txt
            return
        elif txt == '':
            return
        elif txt[0].isalpha() :
            oldtxt = txt
            return
        else:
            oldtxt = txt
            txt=txt.replace(" ", "")
            #print('Next: ' + txt)

            pattern = re.compile(r'-?\d4\d[\>|\<|\=]-?\d\d?')
            if pattern.match(txt):
                if(txt[1] == '4' or txt[2] == '4'):
                    txt = txt.replace('4', '+')
            
            pattern = re.compile(r'-?\d4?t?[+-|\*|\#]\d[\>|\<|\=]-?\d\d?')
            if pattern.match(txt):
                if(txt[1] == 't' or txt[2] == 't'):
                    txt = txt.replace('t', '')
                if((txt[1] == '*' or txt[2] == '*') or (txt[1] == '*')):
                    txt = txt.replace('*', '+')
                if((txt[3] == '#') or (txt[2] == '#') or (txt[1] == '#')):
                    txt = txt.replace('#', '+')
                pattern = re.compile(r'-?\d4[+-|\*|\#]\d[\>|\<|\=]-?\d\d?')
                if pattern.match(txt):
                    if((txt[2] == '4' and txt[3] == '+') or (txt[1] == '4' and txt[2] == '+' )):
                        txt = txt.replace('4+', '+')
                results = txt.find('=')
                if results >= 0:
                    txt = self.insert_equal(txt, results)
                #if txt[-1] == 'O':
                #    txt = txt.replace('O', '')
                #print('Final: ' + txt)
                if eval(txt):
                    pyautogui.click(x=250, y=500)
                    pyautogui.moveTo(x=275, y=500)
                    #time.sleep(.00002)
                    print('T')
                    return
                else:
                    pyautogui.click(x=300, y=500)
                    pyautogui.moveTo(x=275, y=500)
                    #time.sleep(.00002)
                    print('F')
                    return
            else:
                return
            
        

#broke on 3-9<-7
def main():
    imaging = Imaging()
    x = config['x_cord']
    y = config['y_cord']
    offx = config['off_x']
    offy = config['off_y']
    while(True):


        img = ImageGrab.grab(bbox=(x, y, x + offx, y + offy))
        #img = img.resize((new_size_x, new_size_y), Image.ANTIALIAS)
        #helping with image processing
        
        
        img = np.array(img)
       # img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY )[1]
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray = cv2.bitwise_not(gray)
        img = gray
        kernel = np.ones((2, 1), np.uint8)
        img = cv2.erode(img, kernel, iterations=1)
        img = cv2.dilate(img, kernel, iterations=1)


        scale_percent = random.randint(157, 160) # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
       
        
        #img = cv2.resize(img, None, fx = random.randint(1, 2), fy = random.randint(1, 2), interpolation=cv2.INTER_AREA)
        img = cv2.resize(img, dim) 
    # interpolation = cv2.INTER_LINEAR
        cv2.imshow('TalkU', img)
        imaging.process(img)
        
        if cv2.waitKey(25) & 0xFF == ord('q'):  
            cv2.destroyAllWindows()
            break

        
if __name__ == '__main__':
    main()
