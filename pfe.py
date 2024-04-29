import cv2
import pytesseract
import pandas as pd
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
        return None
def compare_matricule(matricule_capture,df ):
    if matricule_capture in df['matricule'].values:
         return true
    else:
            return false 

def capture_matricule(image_path):
    # Chargement de l'image avec OpenCV
    image = cv2.imread(image_path)

    # Conversion en niveaux de gris
 
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Utilisation de Tesseract pour extraire le texte
    matricule = pytesseract.image_to_string(gray_image)

    return matricule.strip()
def detecter_capture():
    
        harcascade = "haarcascade_russian_plate_number.xml"
        plate_detector = cv2.CascadeClassifier(harcascade)
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
                    cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.putText(frame, "Contour", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(frame, "Edge", (x + w - 50, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Edges and Contours", frame)
            
            if cv2.imwrite("matricu.jpg",frame):
                break
        cap.release()
        cv2.destroyAllWindows()

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
    detecter_capture()
    matricule = capture_matricule(image_path)
    print("Matricule detecte :", matricule)
    
    allumer_led(matricule)
