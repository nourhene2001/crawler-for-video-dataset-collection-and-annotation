import json
import os
import cv2
import torch
import cvzone
from ultralytics import YOLO
import math

# Load YOLOv8 model
model = YOLO("yolov8m.pt")
device = model.device
print(device)
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
                x1,y1,x2,y2=box.xyxy[0]
                x1,y1,x2,y2=int(x1),int(y1),int(x2),int(y2)
                
                cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,255),3)
                        #confidence
                conf=math.ceil((box.conf[0]*100))/100
                        
                        #class name
                cls=int(box.cls[0])
                
                name=model.names[cls]
                
                cvzone.putTextRect(frame,f'{name} {conf}',(max(35,x1),max(35,y1)),scale=1,thickness=1)
                c.append(name)
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
cv2.destroyAllWindows()




def annotation (folder):
    # Load YOLOv8 model
    model = YOLO("yolov8m.pt")

 
    #get all videos in dataset
    dataset_folder = os.listdir(folder)
    for video in dataset_folder:
        cap = cv2.VideoCapture(dataset_folder+video)

    

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
                        x1,y1,x2,y2=box.xyxy[0]
                        x1,y1,x2,y2=int(x1),int(y1),int(x2),int(y2)
                        
                        cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,255),3)
                                #confidence
                        conf=math.ceil((box.conf[0]*100))/100
                                
                                #class name
                        cls=int(box.cls[0])
                        
                        name=model.names[cls]
                        
                        cvzone.putTextRect(frame,f'{name} {conf}',(max(35,x1),max(35,y1)),scale=1,thickness=1)
                        c.append(name)
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
        # Add video name and corresponding dictionary to results
        results[video] = my_dict
                # Release everything
        cap.release()
        cv2.destroyAllWindows()
      # Write results to a JSON file
        with open('results.json', 'w') as f:
            json.dump(results, f)
    return my_dict
