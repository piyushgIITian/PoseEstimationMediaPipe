## Instructions to start the programe

git clone https://github.com/piyushgIITian/PoseEstimationMediaPipe

cd rootally

activate your virtual env or install in the base directory

run: pip install -r requirements.txt

run: python .\run.py


## Tasks:
                
1. Write a robust algorithm to calculate successful rep count for knee bend exercise (Use mediapipe  pose model for this task)
2. Add a holding timer limit of 8 sec
3. Include feedback logic in your code, which should be triggered only when a person fails to stay in holding position till 8 sec.
   Feedback message - “Keep your knee bent”
4. Run your code with provided video and upload the full recorded pose detected video in drive.

Exercise description -  
- Leg should be bent to start timer
- Slight inward bend is enough to start the timer. ( <140 deg)
- After a successful rep, the person has to stretch his/her leg straight.
- No restriction for back angle
- Consider leg closer to camera as exercised leg 
