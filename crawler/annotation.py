import json
import os
import cv2
import numpy as np
import torch
import cvzone
from ultralytics import YOLO
import math
import supervision as sv

"""from roboflow import Roboflow
rf = Roboflow(api_key="vt1WopMNT1DHN0D3Ml56")
project = rf.workspace("pfe-ihifb").project("football-players-detection-3zvbc")
dataset = project.version(1).download("yolov8")"""


"""from segment_anything import sam_model_registry, SamPredictor

from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

# Load YOLOv8 model
model = YOLO("yolov8m.pt")

cap = cv2.VideoCapture('crawler\cats.mp4')
print('video')
c=[]
while(cap.isOpened()):
    print('opened')
            # Read a frame from the video file
    ret, frame = cap.read()
    print(ret)
    
    if ret == True:
                # Perform preprocessing on the frame
                # For example, you can resize the frame to a fixed size
        frame = cv2.resize(frame, (640, 480))
                # You can also convert the color space of the frame if needed
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                #peform yolo object detection
        results=model(frame, stream=True)
        for r in results:
                    
            boxes= r.boxes
            for box in boxes:
                        #bouding box
                x1,y1,x2,y2=box.xyxy[0].tolist()
                x,y,w,h=box.xywh[0].tolist()
                x1,y1,x2,y2=int(x1),int(y1),int(x2),int(y2)
                x,y,w,h=int(x),int(y),int(w),int(h)
                cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,255),3)
                        #confidence
                conf=math.ceil((box.conf[0]*100))/100
                        
                        #class name
                cls=int(box.cls[0])
                
                name=model.names[cls]
                
                cvzone.putTextRect(frame,f'{name} {conf}',(max(0,x1),max(35,y1)),scale=1,thickness=1)
                c.append(name)
                box = np.array([
                x, 
                y, 
                x + w, 
                y + h
            ])
                #cv2.imshow('frame',frame)
                
                

                
                
                cv2.imshow('frame',frame)
        # Exit the loop if the 'q' key is pressed or if the video ends
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
my_dict = {}

for item in c:
    if item in my_dict:
        my_dict[item] += 1
    else:
        my_dict[item] = 1
print(c) 
        # Release everything
cap.release()
cv2.destroyAllWindows()"""




"""def annotation(folder):
    # Load YOLOv8 model
    model = YOLO("yolov8m.pt")

    print(folder)

    # Create an empty dictionary to store the results
    res = {}
    
   

    # Get all videos in dataset
    dataset_folder = os.listdir(folder+"\\before")
    output_folder = folder+"\\after"
    os.makedirs(output_folder)
    for video in dataset_folder:
        print(video)
        cap = cv2.VideoCapture(os.path.join(folder+"\\before", video))
        
        # Define the codec and create VideoWriter object
        output_path = os.path.join(output_folder, video)
        cap_out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'),cap.get(cv2.CAP_PROP_FPS), (640, 480), isColor=True)
        c = {}
        while(cap.isOpened()):
            # Read a frame from the video file
            ret, frame = cap.read()
            print(ret)
            # Create VideoWriter object
            
            if ret == True:
                # Perform preprocessing on the frame
                # For example, you can resize the frame to a fixed size
                frame = cv2.resize(frame, (640, 480))

                # Perform YOLO object detection
                results = model(frame)
                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        # Get the class name
                        cls = int(box.cls[0])
                        name = model.names[cls]

                        # Add the class name to the dictionary
                        if name in c:
                            c[name] += 1
                        else:
                            c[name] = 1

                        # Draw bounding box and class label on the frame
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
                        conf = math.ceil((box.conf[0]*100))/100
                        if conf > 0.87:
                            cvzone.putTextRect(frame, f'{name} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
                
                

                
                print("done to out")
                cap_out.write(frame)
            else:
                break
        else:
            break        
               
            

        # Add video name and corresponding dictionary to results
        res[video] = c
        print(res)
        # Release the video capture object
        cap.release()
        cap_out.release()
    # Write results to a JSON file
   
    return res"""
    