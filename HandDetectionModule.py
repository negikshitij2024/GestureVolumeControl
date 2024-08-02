import cv2
import time
import mediapipe as mp

class handDetector():
    def __init__(self, mode=False, maxHands=2,detectionConf=0.5,trackConf=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionConf=detectionConf
        self.trackConf=trackConf

        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionConf,
            min_tracking_confidence=self.trackConf)
        self.mpDraw=mp.solutions.drawing_utils

        
    def findHands(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self,img,handNo=0,draw=True):
        lmList=[]

        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)

        return lmList



def main():
    cap=cv2.VideoCapture(0)
    ctime=0
    ptime=0
    detector=handDetector()
    while True:
        success, img=cap.read()

        img=detector.findHands(img)
        lmlist=detector.findPosition(img)
        if len(lmlist)>0:
            print(lmlist[4])

        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),3)
        cv2.imshow("image",img)

        cv2.waitKey(1)


if __name__ == "__main__":
    main()