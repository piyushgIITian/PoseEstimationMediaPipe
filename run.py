################################
## Importing Libraries
################################
import cv2
import mediapipe as mp
import time
import math

################################
## calculating angle between vectors
################################
def angle_of_vectors(a,b,c,d):
     dotProduct = a*c + b*d
     modOfVector1 = math.sqrt( a*a + b*b)*math.sqrt(c*c + d*d) 
     angle = dotProduct/modOfVector1
     angleInDegree = math.degrees(math.acos(angle))
     return angleInDegree

################################
## mediapipe pose model instanciation
################################
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
################################
## video capture and codec
################################
cap = cv2.VideoCapture('test_video.mp4')
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (width, height))
################################
## Variables
################################
pTime = 0
bent  = False
position = None
message = "Bend your knee to start reps"
counter = 0
bentTimer = False
max_knee_bent = 180
max_time_bent = 0
fluctuations = 0
################################
while True:
    try:
        ## Starting video capture
        success, img = cap.read()
        if success:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            ## Drawing the landmarks
            results = pose.process(imgRGB)
            if results.pose_landmarks:
                mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            ## Storing landmarks points
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                points[id] = (cx,cy)

            for t in range(23,29):
                cv2.circle(img, points[t], 5, (255,0,0), cv2.FILLED)
            ## Calculating Knee AngleInDegree
            kneeAngle = 180 - angle_of_vectors(points[25][0]-points[23][0],points[25][1]-points[23][1],points[27][0]-points[25][0],points[27][1]-points[25][1])
            
            ## Storing current Time
            c_time = time.time()
            ## Checking if knee is bent
            if(not bent and kneeAngle<140):
                position  = "kneeBent"
                bent =  True
                bentTimer = True
                s_time = time.time()
            ## checking if knee is straightened
            elif (kneeAngle>150):
                position  = "kneeStraight"
                bent  = False
            ## Displaying message to user

            if bent and c_time - s_time <= 8 and bentTimer :
                message = "Keep your knee bent"

            if bentTimer and c_time-s_time>=8:
                if kneeAngle>150:
                    counter +=1
                    bentTimer = False
                if c_time-s_time > max_time_bent:
                    max_time_bent  = c_time-s_time
                message = "You can straighten your knee"
            if kneeAngle < max_knee_bent:
                max_knee_bent = kneeAngle
                
            # print(kneeAngle)
            cv2.putText(img, "Knee position: "+ position, (50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
            cv2.putText(img, "message: "+ message, (50,100), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
            cv2.putText(img, "counter: "+ str(counter), (50,150), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)

            ## calculating fps of the videoCapture
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv2.putText(img, "FPS:"+str(round(fps)), (10,600), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0), 3)
            cv2.imshow("Image", img)
            out.write(img)
            k = cv2.waitKey(1)
            if(k == ord('s')):
                break
        else:
            break
    except Exception as e:
        print(e)
        fluctuations+=1
## releasing videoCapture
cap.release()
out.release() 
cv2.destroyAllWindows()

print("######### performance of the user ################")
print("maximum the knee can bend in degrees "+str(max_knee_bent))
print("no. of reps  done " + str(counter))
print("maximum time the knee was bend "+ str(max_time_bent))
print("no. of fluctuations done " + str(fluctuations))
lines = ["######### performance of the user ################","maximum the knee can bend in degrees "+str(max_knee_bent),"no. of reps  done " + str(counter),"maximum time the knee was bend "+ str(max_time_bent),"no. of fluctuations done " + str(fluctuations)]
with open('performance.txt', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')