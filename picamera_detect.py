import cv2
import time
import pyfirmata

port = 'COM4' # 아두이노 포트 설정
board = pyfirmata.Arduino('/dev/ttyACM0')   # firmata와 Arduino 통신 가능하도록 연결 

speaker = board.get_pin('d:13:o')  # 디지털핀 13번을 스피커 출력 핀으로 설정

video = cv2.VideoCapture(0)   # picamera에서 실시간 영상 가져오기, videocapture의 인자는 연결된 카메라 정보 
face_cascade = cv2.CascadeClassifier('/home/antraxmin/opencv-4.1.1/data/haarcascades/haarcascade_frontalface_default.xml')
video.set(3, 640)  # 화면 가로 크기 설정 
video.set(4, 480)  # 화면 세로 크기 설정

while(True):
    ref, frame = video.read()     # 카메라의 상태와 프레임 정보 인받아오기   
	
    frame = cv2.flip(frame,1)   # 좌우 반전 = 1, 상하반전 = 0
    if not ref:     # 카메라가 정상적으로 동작하지 않는다면 
        print("영상을 불러올 수 없습니다. 프로그램을 종료합니다.")
        break
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, 1.4, 5)

    for (x,y,w,h) in face:         # 얼굴 인식하기 
         cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)   # 빨간 사각형으로 표시 
         print('얼굴이 인식되었습니다. 침입자가 들어온 것으로 의심됩니다.')  
         speaker.write(1)       # 경고음 작동
         time.sleep(1)
         speaker.write(0)

    cv2.imshow('picamera_detection',frame)       # 실시간 영상 화면에 보여주기  
    if cv2.waitKey(1) == ord('q'):      # q 입력하면 종료 
        print('프로그램을 종료합니다.')
        break
        
video.release()
cv2.destroyAllWindows()
