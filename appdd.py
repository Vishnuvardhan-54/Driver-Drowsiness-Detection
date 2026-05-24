import cv2
import pygame
import time
import mediapipe as mp
import math

prev_time = time.time()
screenshot_taken = False
alarm_on = False


def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

#HAARDCASCADE PATH
face_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
eye_path = cv2.data.haarcascades + "haarcascade_eye.xml"

#LOAD CASCADES
face_cascade = cv2.CascadeClassifier(face_path)
eye_cascade = cv2.CascadeClassifier(eye_path)

#CAMERA SETUP
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#DROWSINESS SETUP
counter = 0
status =  "ACTIVE"
EAR_THRESHOLD = 0.25

#EYE LANDMARKS
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

#PYGAME & FACEMESH
pygame.mixer.init()
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

#MAIN LOOP
while True:
    head_status= "CENTER"
    ret, frame = camera.read()
    #FPS CALCULATION
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    #FACE DETECTION
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )
    #FACE LANDMARK DETECTION
    if results.multi_face_landmarks:
       for face_landmarks in results.multi_face_landmarks:
          #NOSE TRACKING
          nose = face_landmarks.landmark[1]
          nose_x = int(nose.x * frame.shape[1])
          nose_y = int(nose.y * frame.shape[0])
          
          cv2.circle(frame, (nose_x, nose_y), 5, (255, 0, 255), -1)
           # DRAW FACIAL LANDMARKS
          for landmark in face_landmarks.landmark:
            x = int(landmark.x * frame.shape[1])
            y = int(landmark.y * frame.shape[0])

            cv2.circle(frame, (x, y), 1, (0, 255, 255), -1)

            #HEAD DIRECTION DETECTION
            if nose_x < 200:
                head_status = "LOOKING LEFT"

            elif nose_x > 400:
                head_status = "LOOKING RIGHT"

            elif nose_y > 300:
                pygame.mixer.music.load("alarm.wav")
                pygame.mixer.music.play()
                head_status = "DOWN"

                cv2.putText(
                      frame,
                    "HEAD DOWN ALERT!",
                    (50, 200),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

                pygame.mixer.music.play()

            else:
               head_status = "CENTER"    

            #EYE ASPECT RATIO (EAR)
            left = face_landmarks.landmark
            left_eye = LEFT_EYE

            horizontal = distance(left[left_eye[0]], left[left_eye[3]])
            vertical = distance(left[left_eye[1]], left[left_eye[5]])

            ear = vertical / horizontal
            print("EAR:", ear)

            #DROWSINESS DETECTION
            if ear < EAR_THRESHOLD:
               counter += 1
            else:
               counter=0
               screenshot_taken = False
               pygame.mixer.music.stop()

              
    # FACE & EYE DRAWING
    for (x, y, w, h) in faces:
        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (255, 0, 0),
            2
        )

        face_gray = gray[y:y+h, x:x+w]
        face_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(face_gray)
       

        for (ex, ey, ew, eh) in eyes:
           cv2.rectangle(
           face_color,
           (ex, ey),
           (ex+ew, ey+eh),
           (0, 255, 0),
            2
          )
           
           # ALARM LOGIC
        if counter > 100:
            status = "SLEEPY"

            cv2.putText(
                 frame,
                "WAKE UP DRIVER!",
                (50, 250),
                 cv2.FONT_HERSHEY_SIMPLEX,
                1,(0, 0, 255), 3
                )
          
            
            if not alarm_on:
               pygame.mixer.music.load("alarm.wav")
               pygame.mixer.music.play(-1)
                
               alarm_on = True
             
             #SCREENSHOT CAPTURE
            if not screenshot_taken: 
                filename = f"drowsy_{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                screenshot_taken = True
        else:
           status = "ACTIVE"
           counter = 0
           screenshot_taken = False
           pygame.mixer.music.stop()
           alarm_on = False
    
    #DISPLAY FPS
    cv2.putText(
    frame,
    f"FPS: {int(fps)}",
    (50, 100),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (255, 255, 255),
    2
    )
    #DISPLAY STATUS
    cv2.putText(
    frame,
    f"Status: {status}",
    (50, 150),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (0, 255, 0),
    2
    )    
    #DISPLAY HEAD STATUS
    cv2.putText(
    frame,
    f"Head: {head_status}",
    (50, 200),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (255, 0, 255),
    2
    )
    #SHOW OUTPUT WINDOW
    cv2.imshow("Driver Monitor", frame)
     # EXIT KEY
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#RELEASE CAMERA
camera.release()
cv2.destroyAllWindows()