import cv2
import time
import threading
import DobotDllType as dType

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll
api = dType.load()

#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])



cap=cv2.imread('yolo4.png',0)
cv2.imshow('asdsa',cap)
ret,thresh1 = cv2.threshold(cap,127,255,cv2.THRESH_BINARY)
resized=cv2.resize(thresh1,(400,300))
cv2.imshow('asd',resized)
    
if (state == dType.DobotConnect.DobotConnect_NoError):

    #Clean Command Queued
    dType.SetQueuedCmdClear(api)

    #Async Motion Params Setting
    dType.SetHOMEParams(api, 200, 0, 136, 0, isQueued = 1)
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
    dType.SetPTPJumpParams(api,4,-55,isQueued=1)

    count=0

    for i in range(300):
        for j in range(400):
            
            if(resized[i,j]==0):
                print(i,j)
                
                lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, 300-((float(i*100)/float(300))), 80-((float(j*160)/float(400))), -59, 0, isQueued = 1)[0]
                
                count=count+1
                print(count)
            if(count==25):
                dType.SetQueuedCmdStartExec(api)

                #Wait for Executing Last Command 
                while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
                    dType.dSleep(100)
		
                #Stop to Execute Command Queued
                dType.SetQueuedCmdStopExec(api)
                dType.SetQueuedCmdClear(api)
                count=0
           
    #Start to Execute Command Queued
    print("END")
    dType.SetQueuedCmdStartExec(api)

    #Wait for Executing Last Command 
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)
		
    #Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api)

cv2.waitKey(0)
#Disconnect Dobot
dType.DisconnectDobot(api)
cv2.destroyAllWindows()
