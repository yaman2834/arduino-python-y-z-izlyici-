
#OpenCV ve Arduino kullanarak yuz izleyici
# Ali Yaman tarafindan

import cv2    # Open cv kutuphanesi kurulur 
import serial,time # pyserial kÃ¼tÃ¼panesini kurup tanmÄ±mlÄ±yoruz  
face_cascade= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  #https://github.com/opencv/opencv/tree/master/data/haarcascades  
cap=cv2.VideoCapture(0)
fourcc= cv2.VideoWriter_fourcc(*'XVID')
ArduinoSerial=serial.Serial('com4',9600,timeout=0.1) #Ardino ile iletisimi saglanýr (sizin port larÄ±nÄ±z farklÄ± olabilir  )
out= cv2.VideoWriter('face detection4.avi',fourcc,20.0,(640,480))
time.sleep(1)

while cap.isOpened():
    ret, frame= cap.read()
    frame=cv2.flip(frame,1) 
    print(frame.shape)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces= face_cascade.detectMultiScale(gray,1.1,6)  
    for x,y,w,h in faces:
    #Arduino'ya koordinat gonderme 
        string='X{0:d}Y{1:d}'.format((x+w//2),(y+h//2))
        print(string)
        ArduinoSerial.write(string.encode('utf-8'))
       
        cv2.circle(frame,(x+w//2,y+h//2),2,(0,255,0),2)
        
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
   
    cv2.rectangle(frame,(640//2-30,480//2-30),
                 (640//2+30,480//2+30),
                  (255,255,255),3)
    out.write(frame)
    cv2.imshow('img',frame)
    cv2.imwrite('output_img.jpg',frame)
    '''for test iÃ§in 
    read= str(ArduinoSerial.readline(ArduinoSerial.inWaiting()))
    time.sleep(0.05)
    print('data from arduino:'+read)
    '''
 
    if cv2.waitKey(10)&0xFF== ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# Gelen ekraný± kapatmak icýn q tusŸuna basiniz 
#END :)