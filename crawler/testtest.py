#craete project in roboflow with yolo for object detection
#add frame
import json
import math
import cv2
import roboflow
from roboflow import Roboflow
import os
import cvzone
rf = Roboflow(api_key="vt1WopMNT1DHN0D3Ml56")
project = rf.workspace().project("yolo-m1mve")
model = project.version(1).model
# Open the video file
video_path = "crawler\\1.mp4"
#cap = cv2.VideoCapture(video_path)
cap = cv2.VideoCapture(video_path)

# Define the path to save the frames
save_path = "crawler\\temp_img"

# Create the directory if it does not exist
if not os.path.exists(save_path):
    os.makedirs(save_path)
output_folder="crawler\\video"
output_path = os.path.join(output_folder, "video.mp4")
print(output_path)
cap_out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'),cap.get(cv2.CAP_PROP_FPS), (640, 640), isColor=True)
# Loop through the frames and save them as JPEG files
frame_count = 0
# Initialize an empty dictionary to store the object timestamps
object_timestamps = {}
data = {
    "info": {
        "video name":"1.pm4",
        "description": "Video annotation using YOLO model",
        "year": 2023,
        "version": "1.0",
        "contributor": "nourhene",
        "date_created": "2023-05-04",
        "duration in seconds" : "6"
    },
    "video": [],
    "annotations": [],
    "timestamps": []
}
while (cap.isOpened()):
    # Read the next frame
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (640, 640))
    # Save the frame as a JPEG file
    frame_path = os.path.join(save_path, f"frame_{frame_count:04d}.jpg")
    cv2.imwrite(frame_path, frame)
    
    predictions=model.predict(frame_path, confidence=80, overlap=30).json()
    print(predictions)
    wh=[]
    wh.append({
            
            "width": predictions['image']['width'],
            "height": predictions['image']['height'],
            
            })
    # Increment the frame count
    frame_count += 1
    frame_t = cv2.imread(frame_path)
    for r in predictions["predictions"]:
        x0 = r['x'] - r['width'] / 2
        x1 = r['x'] + r['width'] / 2
        y0 = r['y'] - r['height'] / 2
        y1 = r['y'] + r['height'] / 2
        conf=r['confidence']
        classe=r['class']
        start_point = (int(x0), int(y0))
        end_point = (int(x1), int(y1))
    # Calculate the timestamp for this frame
        cv2.rectangle(frame_t, start_point, end_point, color=(0,255,0), thickness=1)
        conf = math.ceil(conf*100)/100
        cvzone.putTextRect(frame_t, f'{conf} {classe}', (int(x0)-5, int(y0)-10), scale=1, thickness=1)
        timestamp = frame_count / cap.get(cv2.CAP_PROP_FPS)
        
        
        # Check if this object has been seen before
        object_id = f"{classe}"
        if object_id in object_timestamps:
            # This object has been seen before, update its end timestamp
            object_timestamps[object_id][-1] = (object_timestamps[object_id][-1][0], timestamp)
        else:
            # This is a new object, add it to the dictionary
            object_timestamps[object_id] = [(timestamp, timestamp)]
        predictions_list=[]
        predictions_list.append({
        
        'frame': frame_count,
        'predictions': predictions, 
        'bounding_boxes': (int(x0), int(y0),int(x1), int(y1)),
        
        })
     
     
        # Append the prediction to the list
        if predictions_list:
            data['timestamps'] =  object_timestamps

            for p in predictions_list:
                
                for pred in p['predictions']['predictions']:
                    
                    bbox = (int(x0), int(y0),int(x1), int(y1))
                    annotation = {
                                    "id": len(data['annotations']) + 1,
                                    "frame_id": p['frame'],
                                    "object":pred['class'],
                                    "confidence":pred['confidence'],
                                    "bbox": bbox,
                                    
                        }
                    data['annotations'].append(annotation)




        


                    
                
            cv2.imwrite("example_with_bounding_boxes.jpg", frame_t)
            cap_out.write(frame_t)
        # Print the object timestamps
data['video'].append({
    "width": wh[0]['width'],
    "height": wh[0]['height']
})
print(object_timestamps)
    
# Release the video capture object and close all windows
cap.release()
cap_out.release()
cv2.destroyAllWindows()
with open('annotations.json', 'w') as f:
    json.dump(data, f)



"""workspace = Roboflow(api_key='vt1WopMNT1DHN0D3Ml56').workspace()
new_project = workspace.create_project(
    project_name='yolo',
    project_license="MIT",
    project_type="object-detection", 
    annotation="yolov8"
    )
conf={
    "augmentation": {
        "crop": {
            "min": 0,
            "max": 71
        }
    },
    "preprocessing": {
        "auto-orient": True
    }
}

version_number=new_project.generate_version(conf)
version = new_project.version(version_number)
new_project.upload("crawler\\two-cigarettes-13262319.jpg")
version.deploy(model_type='yolov8', model_path=f'crawler\\yolov8\\')
model=version.model"""