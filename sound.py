import cv2
import mediapipe as mp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
print(volume.GetMasterVolumeLevel())
#volume.GetMasterVolumeLevel()
#print(volume.GetVolumeRange())
volume.SetMasterVolumeLevel(-21.0,None)

cap=cv2.VideoCapture(0)
mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils

while True:
    success,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
   # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmlist=[]
            for id,lm in enumerate(handLms.landmark):
                #print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
               # print(id,cx,cy)
                lmlist.append([id,cx,cy])
                #print(lmlist)
                mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
        if lmlist:
              x1,y1=lmlist[4][1],lmlist[4][2]
              x2,y2=lmlist[8][1],lmlist[8][2]
              cv2.circle(img,(x1,y1),10,(255,0,9),cv2.FILLED)
              cv2.circle(img, (x2, y2), 10, (255, 0, 9), cv2.FILLED)
              cv2.line(img,(x1,y1),(x2,y2),(24,86,127),3)
              length=math.hypot(x2-x1,y2-y1)
             # print(length)
        if length<50:
             z1=(x1+x2)//2
             z2=(y1+y2)//2
             cv2.circle(img,(z1,z2),10,(255, 0, 9),cv2.FILLED)
        volRange=volume.GetVolumeRange()
        minVol=volRange[0]
        maxVol=volRange[1]
        vol=np.interp(length,[50,300],[minVol,maxVol])
        volBar=np.interp(length,[50,300],[400,150])
        volPer=np.interp(length,[50,300],[0,100])
        volume.SetMasterVolumeLevel(vol, None)
        cv2.rectangle(img,(50,150),(85,400),(126,58,234),3)
        cv2.rectangle(img,(50,int(volBar)),(85,400),(126,58,234),cv2.FILLED)
        cv2.putText(img,str(int(volPer)),(40,100),cv2.FONT_HERSHEY_COMPLEX,4,(126,58,234))


    cv2.imshow("Image",img)
    key=cv2.waitKey(1)
    if key==ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
#length 50-300
#volRange -24 to +21