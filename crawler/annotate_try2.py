#craete project in roboflow with yolo for object detection
#add frame
import math
import cv2
import numpy as np
import roboflow
from roboflow import Roboflow
import os
import cvzone
import torch
from segment_anything import sam_model_registry
from segment_anything import SamPredictor
import supervision as sv
"""
DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
MODEL_TYPE = "vit_h"
CHECKPOINT_PATH="crawler\sam_vit_h_4b8939.pth"
sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH)
mask_predictor = SamPredictor(sam)
sam.to(device=DEVICE)
mask_annotator = sv.MaskAnnotator(color=sv.Color.red())

rf = Roboflow(api_key="vt1WopMNT1DHN0D3Ml56")
project = rf.workspace().project("yolo-9lug8")
model = project.version(1).model
# Open the video file
video_path = "crawler\cats.mp4"
cap = cv2.VideoCapture(video_path)

# Define the path to save the frames
save_path = "crawler\\temp_img"

# Create the directory if it does not exist
if not os.path.exists(save_path):
    os.makedirs(save_path)
output_folder="crawler\\video"
output_path = os.path.join(output_folder, "video.mp4")
print(output_path)
cap_out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'),cap.get(cv2.CAP_PROP_FPS), (640, 480), isColor=True)
# Loop through the frames and save them as JPEG files
frame_count = 0
while (cap.isOpened()):
    # Read the next frame
    ret, frame = cap.read()
    if not ret:
        break
    
    # Save the frame as a JPEG file
    frame_path = os.path.join(save_path, f"frame_{frame_count:04d}.jpg")
    cv2.imwrite(frame_path, frame)
    
    predictions=model.predict(frame_path, confidence=60, overlap=30).json()
    print(predictions)
    # Increment the frame count
    frame_count += 1
    frame_t = cv2.imread(frame_path)
    # Access JSON record for the image width
    w=predictions['image']['width']

    # Access JSON record for the image height
    h=predictions['image']['height']
    for r in predictions["predictions"]:
        x0 = r['x'] - r['width'] / 2
        x1 = r['x'] + r['width'] / 2
        y0 = r['y'] - r['height'] / 2
        y1 = r['y'] + r['height'] / 2
        conf=r['confidence']
        classe=r['class']
        start_point = (int(x0), int(y0))
        end_point = (int(x1), int(y1))
                  
        cv2.rectangle(frame_t, start_point, end_point, color=(0,255,0), thickness=1)
        conf = math.ceil(conf*100)/100
        
        cvzone.putTextRect(frame_t, f'{conf} {classe}', (int(x0)-5, int(y0)-10), scale=1, thickness=1)
        image_rgb = cv2.cvtColor(frame_t, cv2.COLOR_BGR2RGB)
        mask_predictor.set_image(image_rgb)
        box = np.array([
           r['x'] /2 , 
            r['y'] /2 ,
            x1  ,
            y1 
        ])
        masks, scores, logits = mask_predictor.predict(
            box=box,
            multimask_output=True
        )
        detections = sv.Detections(
            xyxy=sv.mask_to_xyxy(masks=masks),
            mask=masks
        )

        detections = detections[detections.area == np.max(detections.area)]
        segmented_image = mask_annotator.annotate(scene=frame_t.copy(), detections=detections)
    cv2.imwrite("example_with_bounding_boxes.jpg", segmented_image)

    cap_out.write(frame_t)
# Release the video capture object and close all windows
cap.release()
cap_out.release()
cv2.destroyAllWindows()"""
#delete the temp folder