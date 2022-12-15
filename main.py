import numpy as np
import cv2
# import winsound

# picamera 설정
#capture = cv2.VideoCapture(0)  # 비디오 출력 클래스로 picamera 모듈에서 정보를 받아오도록 설정 - VideoCapture()의 인자는 카메라의 장치 번호(ID) 
#capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 카메라 사이즈 설정 ( 640 x 480 ) 
#capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# picamera에서 프레임 전달받기
#while cv2.waitKey(33) < 0:      # 임의의 키 입력 전까지 33ms마다 반복문 실행 
#    ref, frame = capture.read()     # 카메라의 상태와 프레임 받아오기 (ref - 카메라의 상태 저장(정상True, 비정상False) / frame - 현재 시점의 프레임 저장)
#    cv2.imshow("VideoFrame", frame) # 이미지 표시 함수 - 특정 윈도우 창에 이미지 띄우기 => imshow("윈도우 창의 제목", 표시할 이미지) 

classes = []
f=open('coco.names.txt','r')
classes=[line.strip() for line in f.readlines()]
colors=np.random.uniform(0,255,size=(len(classes),3))

yolo_model=cv2.dnn.readNet('yolov3.weights','yolov3.cfg') # 욜로 읽어오기
layer_names=yolo_model.getLayerNames()
out_layers=[layer_names[i-1] for i in yolo_model.getUnconnectedOutLayers()]

def process_video(): # 비디오에서 침입자 검출해 알리기
    video=cv2.VideoCapture(0)    # 비디오 출력 클래스로 picamera 모듈에서 정보를 받아오도록 설정 - VideoCapture()의 인자는 카메라의 장치 번호(ID) 
    while video.isOpened():
        success,img=video.read()    # 카메라의 상태와 프레임 받아오기 (success - 카메라의 상태 저장(정상True, 비정상False) / img - 현재 시점의 프레임 저장)
        if success:                 # 카메라가 정상적으로 동작한다면 (True) 
            height,width,channels=img.shape
            blob=cv2.dnn.blobFromImage(img,1.0/256,(448,448),(0,0,0),swapRB=True,crop=False)

            yolo_model.setInput(blob)
            output3=yolo_model.forward(out_layers)

            class_ids,confidences,boxes=[],[],[]
            for output in output3:
                for vec85 in output:
                    scores=vec85[5:]
                    class_id=np.argmax(scores)
                    confidence=scores[class_id]
                    if confidence>0.5: # 신뢰도가 50% 이상인 경우만 취함
                        centerx,centery=int(vec85[0]*width),int(vec85[1]*height) # [0,1] 표현을 영상 크기로 변환
                        w,h=int(vec85[2]*width),int(vec85[3]*height)
                        x,y=int(centerx-w/2),int(centery-h/2)
                        boxes.append([x,y,w,h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
                    
            indexes=cv2.dnn.NMSBoxes(boxes,confidences,0.5,0.4)
                    
            for i in range(len(boxes)):
                if i in indexes:
                    x,y,w,h=boxes[i]
                    text=str(classes[class_ids[i]])+'%.3f'%confidences[i]
                    cv2.rectangle(img,(x,y),(x+w,y+h),colors[class_ids[i]],2)
                    cv2.putText(img,text,(x,y+30),cv2.FONT_HERSHEY_PLAIN,2,colors[class_ids[i]],2)

            cv2.imshow('Object detection',img)

            if 0 in class_ids: # 사람이 검출됨(0='person')
                print('사람이 나타났다!!!')
                # winsound.Beep(frequency=2000,duration=500)

        key=cv2.waitKey(1) & 0xFF
        if key==27: break

    video.release()     # 카메라 장치에서 받아온 메모리를 해제
    cv2.destroyAllWindows()     # 모든 창 닫기

process_video()
