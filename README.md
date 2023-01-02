# 프로젝트 소개
- 프로젝트명: OpenCV + Raspberry Pi + Arduino를 이용한 실시간 얼굴 인식 CCTV 
- 개발기간: 22.12.12 ~ 22.12.13
- 개발자: 임채민([@Antraxmin](https://github.com/Antraxmin)), 최가현([@hni00](https://github.com/hni00))

<br>

## 🛠️ Tech Stack 
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/RaspberryPi-A22846?style=for-the-badge&logo=RaspberryPi&logoColor=white">
<img src="https://img.shields.io/badge/openCV-5C3EE8?style=for-the-badge&logo=openCV&logoColor=white">
<img src="https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white">
<br><br>

## 프로젝트 구조
> 도난 방지 및 침입 감지 시스템 구축을 위한 IoT CCTV 프로젝트의 초기 버전으로, 지속적인 업데이트를 진행할 예정이다. 
<img src="https://user-images.githubusercontent.com/77287236/210170447-07778d38-6f45-4b98-930c-3aa8db6060cd.JPG"/>


본 프로젝트는 Raspberry Pi, Arduino, OpenCV를 연동하여 실시간으로 침입자를 탐지하는 기능을 제공한다. 
<br> 침입자 발생 시 경보음이 작동하는 원리는 다음과 같다. 
- 라즈베리파이 카메라 모듈인 piCamera를 통해 실시간 영상을 촬영한다.
- 촬영된 영상은 프레임 단위의 객체로 변환되어 OpenCV 영상처리 모델로 전송된다.
- OpenCV Haar Cascades 알고리즘을 사용하여 실시간 영상 프레임에서 침입자의 얼굴 정보를 검출한다. 
- Firmata Protocol 통신을 이용하여 라즈베리파이와 아두이노를 연동하고, 내장된 OpenCV 모델에서 침입자를 인식했을 때 아두이노에 연결된 스피커 센서로 경보음이 작동한다. 

<br><br>

## 💻 개발 기능
> 프로젝트의 모든 기능은 라즈베리파이 3B+에 내장된 Raspbian OS 환경에서 개발하였다. 

<br>

### 목차
- [1. 라즈베리파이와 OpenCV 연동](#1-라즈베리파이와-opencv-연동)
- [2. 라즈베리파이 Camera Module 연결 및 테스트](#2-라즈베리파이-camera-module-연결-및-테스트)
- [3. 얼굴 인식 모델 구현 - picamera_detect.py](#3-얼굴-인식-모델-구현---picamera_detectpy)
- [4. 아두이노-라즈베리파이 연동을 위한 Firmata Protocol 통신 환경 구축](#4-아두이노-라즈베리파이-연동을-위한-firmata-protocol-통신-환경-구축)
- [5. OpenCV 얼굴 인식으로 아두이노 제어](#5-opencv-얼굴-인식으로-아두이노-제어)
<br><br><br>

### 1. 라즈베리파이와 OpenCV 연동
라즈베리파이 상에서 OpenCV를 사용하기 위한 개발 환경을 세팅한다.<br>
개발할 모델은 Python 기반이므로 `pip3`를 이용하여 OpenCV 패키지를 설치한다. 
```
~ $ sudo apt-get update
~ $ sudo apt-get upgrade
~ $ pip3 install opencv-python
~ $ pip install opencv-contrib-python
```
<br><br>

### 2. 라즈베리파이 Camera Module 연결 및 테스트
라즈베리파이에 연결된 piCamera로 실시간 영상을 촬영하기 위해 카메라 모듈을 활성화한다. <br>
```
~ $ sudo raspi-config > Interfacing Options > Camera > Enable
~ $ vcgencmd get_camera
~ $ raspistill -o test.jpg
```
<br><br>

### 3. 얼굴 인식 모델 구현 - picamera_detect.py
> OpenCV와 Python을 기반으로 사람의 얼굴을 인식하는 Computer Vision 모델을 구현하였다. 
<br>

`VideoCapture()`함수로 0번 입력 디바이스인 piCamera와 연결한다. (640 x 480)
```
video = cv2.VideoCapture(0)
video.set(3, 640)  
video.set(4, 480)
```
<br>

`CascadeClassifier()`함수로 `cascade` 학습을 거친 데이터를 불러온다. <br>
cascade 학습은 특징점 기반의 Object 검출 알고리즘인 `Haarcascades`를 이용하였다. <br>
(YOLOv5를 이용해 직접 학습시킬 계획이었으나 라즈베리파이 속도 저하 및 빌드 시간 문제로 인해 미리 학습된 알고리즘 사용)
```
face_cascade = cv2.CascadeClassifier('/home/antraxmin/opencv-4.1.1/data/haarcascades/haarcascade_frontalface_default.xml')
```
<br>

piCamera에 저장된 실시간 영상 데이터를 프레임 단위로 읽어 저장한다. 
```
ref, frame = video.read()       
frame = cv2.flip(frame,1)
```
<br>

이미지 처리 속도 향상을 위해 BGR 형태의 원본 영상 프레임을 __grayScale__ 로 변환하였다. 
```
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```
<br>

grayScale로 변환한 영상 프레임에서 얼굴로 판단되는 부분의 정보를 검출한다. 
`Scalefactor` 값을 1.4배로 설정하여 검출 시간을 단축하고자 하였다. (인식 정확도를 높이려면 `Scalefactor` 값을 낮추면 된다)
```
 face = face_cascade.detectMultiScale(gray, 1.4, 5)
```
<br>

인식된 얼굴의 위치를 찾아 사각형 테두리를 그린다. 
```
cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
```
<br><br>

### 4. 아두이노-라즈베리파이 연동을 위한 Firmata Protocol 통신 환경 구축
해당 프로젝트에서 라즈베리파이는 영상 처리를, 아두이노는 센서 구동을 담당한다. 이때 라즈베리파이와 아두이노를 연동하기 위해 `Firmata` 프로토콜을 이용한 통신 환경을 구축하였다. <br><br>
라즈베리파이 Python 환경에서 `Firmata` 프로토콜을 이용하여 아두이노를 직접 제어하기 위해 `pyFirmata` 패키지를 설치한다.  
```
$ sudo apt-get install python-pip python-serial 
$ sudo pip install pyfirmata 
```

시리얼 통신을 위해 라즈베리파이와 아두이노를 USB로 연결한 후 아두이노에 `StandardFirmata` 라이브러리를 업로드한다. 
<br><br><br>

### 5. OpenCV 얼굴 인식으로 아두이노 제어
picamera_detect.py 파일에 `pyFirmata` 라이브러리를 import 하여 실시간으로 영상을 처리함과 동시에 아두이노를 제어할 수 있도록 설정하였다. <br><br>
아두이노 보드가 연결된 포트 정보를 python 코드에 추가한다.  
 
```
port = 'COM4' 
board = pyfirmata.Arduino('/dev/ttyACM0')
```
<br>

OpenCV를 통해 분석한 실시간 영상 프레임에서 사람의 얼굴이 인식되었다면 아두이노에 연결된 스피커 센서로 경보음이 발생하는 기능을 구현하였다. 
스피커 센서와 연결된 아두이노의 13번 핀을 출력 모드로 설정하고, 얼굴이 인식될 때마다 출력값 1과 0을 번갈아 전송한다.

```
speaker = board.get_pin('d:13:o') 
face = face_cascade.detectMultiScale(gray, 1.4, 5)
    for (x,y,w,h) in face:          
         cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)    
         speaker.write(1)      
         time.sleep(1)
         speaker.write(0)
```
<br><br>

## 결과물
<img src="https://user-images.githubusercontent.com/77287236/210178136-9e385eba-8d71-4a66-aa8f-08f63d43c291.JPG"/>

<br>

## 추후 개선 사항
- YOLOv5를 기반으로 직접 학습 가능한 영상처리 모델 개발
- 정면 얼굴인식 뿐만 아니라 측면 및 후면 얼굴 인식 기능을 추가하여 인식 정확도 개선
- 최종적으로는 서버 및 안드로이드 앱과 연동한 딥러닝 기반 실시간 도난 방지 시스템 구축 예정
