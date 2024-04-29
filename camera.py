import cv2

#print("Before URL")
cap = cv2.VideoCapture('rtsp://admin:Mo123Pfe6@192.168.166.29:554/user=admin&password=Mo123Pfe6&channel=1&stream=0.sdp?')
#print("After URL")

print(cap.isOpened())
while True:

    #print('About to start the Read command')
    ret, frame = cap.read()
    #print('About to show frame of Video.')
    cv2.imshow("Capturing",frame)
    #print('Running..')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
