import cv2
import pytesseract
import pandas as pd
import imutils
import numpy as np

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
# Configuration GPIO
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Configuration Tesseract
pytesseract.pytesseract.tesseract_cmd = 'tesseract'

def read_excel_file(file_path):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None
    except Exception as e:
        print("An error occurred:", e)
        return 
def compare_matricule(matricule_capture,df ):
    if matricule_capture in df['matricule'].values:
         return true
    else:
            return false 

def capture_matricule(image_path):
        Cropped=""
        harcascade = r"./haarcascade_russian_plate_number.xml"
        plate_detector = cv2.CascadeClassifier(harcascade)
        img = cv2.imread(image_path,cv2.IMREAD_COLOR)
        img = cv2.resize(img, (600,400) )

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        gray = cv2.bilateralFilter(gray, 13, 15, 15) 
        edged = cv2.Canny(gray, 30, 200) 
        contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
        screenCnt = None

        for c in contours:
            
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
         
            if len(approx) == 4:
                screenCnt = approx
                break

        if screenCnt is None:
            detected = 0
            text="0"
            
        else:
             detected = 1

        if detected == 1:
            cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

            mask = np.zeros(gray.shape,np.uint8)
            new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
            new_image = cv2.bitwise_and(img,img,mask=mask)

            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))
            Cropped = gray[topx:bottomx+1, topy:bottomy+1]

            text = pytesseract.image_to_string(Cropped, config='--psm 11',lang='fra+ara')
             
            img = cv2.resize(img,(500,300))
            Cropped = cv2.resize(Cropped,(400,200))
           # cv2.imshow('car',img)
            #cv2.imshow('Cropped',Cropped)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return text,Cropped

def detecter_capture(output_path):
    
         
        cap = cv2.VideoCapture('rtsp://admin:Mo123Pfe6@192.168.166.29:554/user=admin&password=Mo123Pfe6&channel=1&stream=0.sdp?')
        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            _, threshold = cv2.threshold(gray_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            morph_opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
            contours, _ = cv2.findContours(morph_opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:
                  #  cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
                    x, y, w, h = cv2.boundingRect(contour)
                #  cv2.putText(frame, "Contour", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                  #  cv2.putText(frame, "Edge", (x + w - 50, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Edges and Contours", frame)
            
            if cv2.imwrite(output_path,frame):
                break
        cap.release()
        cv2.destroyAllWindows()
        return 

def allumer_led(matricule):  
    # Verification du matricule
    if matricule.isdigit() and len(matricule) == 6:
        # Allumer la LED
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        # eteindre la LED
        GPIO.output(LED_PIN, GPIO.LOW)

if __name__ == "__main__":
    image_path = "matricu.jpg"
    matricule="ok"
    print("Matricule detecte :", matricule)
    while True:
        detecter_capture(image_path)
        matricule,img = capture_matricule(image_path)
        if len(matricule) >1:
            print("Matricule detecte :", matricule)
            break
        else: 
            print("Matricule detecte :", matricule)
            
        if len(img)>0:
            cv2.imshow('',img)
    
    allumer_led(matricule)
        
    

