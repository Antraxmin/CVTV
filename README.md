# cv-rpi-cctv
해당 작품은 2022-2 자기주도진로탐색학점제 최종 프로젝트로 개발한 IoT 기반의 Computer Vision 모델입니다. <br><br>
# 프로젝트 소개
- 프로젝트명: OpenCV + Raspberry Pi + Arduino를 이용한 실시간 얼굴 인식 CCTV 
- 개발기간: 22.12.12 ~ 22.12.13
- 개발자: 임채민([@Antraxmin](https://github.com/Antraxmin)), 최가현([@hni00](https://github.com/hni00))

## 🛠️ Tech Stack 
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/RaspberryPi-A22846?style=for-the-badge&logo=RaspberryPi&logoColor=white">
<img src="https://img.shields.io/badge/openCV-5C3EE8?style=for-the-badge&logo=openCV&logoColor=white">
<img src="https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white">
<img src="https://img.shields.io/badge/Anaconda-44A833?style=for-the-badge&logo=Anaconda&logoColor=white"><br><br>


## 💻 상세 구현 목록
> 프로젝트의 모든 기능은 라즈베리파이 3B+에 내장된 Raspbian OS에서 실행됩니다. 

### 1. 라즈베리파이와 OpenCV 연동
- piCamera로 촬영한 실시간 영상 데이터를 라즈베리파이로 전송
- OpenCV `videoCapture` 모듈을 이용하여 영상 데이터가 OpenCV 모델로 전달되도록 설정

### 2. Python + OpenCV 기반의 얼굴 인식 기능 구현
- 특징 기반의 Object 검출 알고리즘인 `Haarcascades`를 이용하여 사람의 얼굴을 인식
- `cv2.rectangle` 모듈을 통해 실시간 영상 데이터로부터 얻어낸 얼굴 객체에 테두리 표시

### 3. Firmata를 이용한 아두이노-라즈베리파이 간의 통신 구현
- 라즈베리파이에 `Firmata` 모듈 설치하여 시리얼 통신 환경 구축
- `pyFirmata`를 이용하여 OpenCV Python에서 `Firmata` 프로토콜로 아두이노를 직접 제어
- 사람의 얼굴이 인식되었다면 아두이노에 연결된 Active Buzzer로 경보음 발생


## 프로젝트 구조


## Demo


## 추후 개선 사항
- YOLOv5 학습 모델 적용 시 라즈베리파이 속도 저하 문제 개선
- 단순한 얼굴 인식 기능을 확장하여 특정인을 인식하도록 구현
- 안드로이드 앱과 연동하여 CCTV 데이터를 스마트폰으로 전송하는 기능 구현



