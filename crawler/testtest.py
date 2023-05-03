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
video_path = "crawler\cats.mp4"
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
        "description": "Video annotation using YOLO model",
        "year": 2023,
        "version": "1.0",
        "contributor": "Your Name",
        "date_created": "2023-05-04"
    },
    "images": [],
    "annotations": [],
    "categories": []
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
    
    predictions=model.predict(frame_path, confidence=60, overlap=30).json()
    print(predictions)
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
        predictions_list=[]
        
        # Check if this object has been seen before
        object_id = f"{classe}"
        if object_id in object_timestamps:
            # This object has been seen before, update its end timestamp
            object_timestamps[object_id][-1] = (object_timestamps[object_id][-1][0], timestamp)
        else:
            # This is a new object, add it to the dictionary
            object_timestamps[object_id] = [(timestamp, timestamp)]
        predictions_list.append({
        'video name':"cat.mp4",
        'frame': frame_count,
        'predictions': predictions,
        'bounding_boxes': (int(x0), int(y0),int(x1), int(y1)),
        'object timestamps':object_timestamps,
        })
    

        # Append the prediction to the list


    categories = []
    for p in predictions_list:
        for pred in p['predictions']['predictions']:
            if pred['class'] not in categories:
                categories.append(pred['class'])

    data['categories'] = [{"id": i+1, "name": c} for i, c in enumerate(categories)]

    for p in predictions_list:
        filename = "frame_{:04d}.jpg".format(p['frame'])
        data['images'].append({
            "id": p['frame'],
            "width": p['predictions']['image']['width'],
            "height": p['predictions']['image']['height'],
            "file_name": filename,
            "date_captured": "2023-05-04"
            })

        for pred in p['predictions']['predictions']:
            category_id = categories.index(pred['class']) + 1
            bbox = (int(x0), int(y0),int(x1), int(y1))
            annotation = {
                    "id": len(data['annotations']) + 1,
                    "image_id": p['frame'],
                    "category_id": category_id,
                    "bbox": bbox,
                    "area": bbox[2] * bbox[3],
                    "iscrowd": 0,
                    "attributes": {},
                    "timestamp": p['object timestamps'][pred['class']][-1]
                }
            data['annotations'].append(annotation)


   


            
        
    cv2.imwrite("example_with_bounding_boxes.jpg", frame_t)
    cap_out.write(frame_t)
        # Print the object timestamps

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