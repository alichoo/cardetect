
import RPi.GPIO as GPIO 
import time
GPIO.setmode(GPIO.BCM)
 
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
print ("led on")
GPIO.output(18,GPIO.HIGH)
GPIO.output(23,GPIO.HIGH)
GPIO.output(27,GPIO.HIGH)
time.sleep(20)
print("LED off")
GPIO.output(18,GPIO.LOW)
#G
GPIO.output(23,GPIO.LOW)   
