import HandDetectionModule as hdm
import cv2
import time
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
print()



volrange=volume.GetVolumeRange()
cap=cv2.VideoCapture(0)
pTime=0
cTime=0
detector=hdm.handDetector(detectionConf=0.7)
volbar=0
while True:


    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime 
    success,img=cap.read()
    img=detector.findHands(img,draw=False)
    lmlist=detector.findPosition(img,draw=False)

    if len(lmlist)>0:

        x1,y1=lmlist[8][1],lmlist[8][2]
        x2,y2=lmlist[4][1],lmlist[4][2]
        cv2.circle(img,(x1,y1),10,(0,255,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(0,255,255),cv2.FILLED)
        mpx,mpy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(mpx,mpy),10,(255,255,255),2)
        dist=np.hypot(x1-x2,y1-y2)
        # print(f"Dist = {dist}")
        cv2.line(img,(x1,y1),(x2,y2),(0,255,255),2)
        if dist<20:
            cv2.circle(img,(mpx,mpy),15,(255,255,255),cv2.FILLED)


        #normalizing the distance range to volume range
        vol=np.interp(dist,[20,160],[volrange[0],volrange[1]])
        
        volbar=np.interp(dist,[20,160],[400,150])
        volper=np.interp(dist,[20,160],[0,100])
        print(vol)
        
        cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
        cv2.rectangle(img,(50,int(volbar)),(85,400),(0,255,0),cv2.FILLED)
        cv2.putText(img,f"Vol : {int(volper)}%",(30,130),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
        # setting the volume
        volume.SetMasterVolumeLevel(vol, None)

    cv2.putText(img,f'FPS {int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cv2.imshow("image",img)
    if cv2.waitKey(1) == ord('q'):
        break

    

#max=160 min=10

#vol range -63.5 , 0.0