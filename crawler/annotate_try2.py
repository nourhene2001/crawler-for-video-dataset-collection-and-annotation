#craete project in roboflow with yolo for object detection
#add frame
import json
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

def annotate_vid(path,author,duration,creation_date,resolution,video_format,views,dataset,description_v,description_d):

    DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    MODEL_TYPE = "vit_h"
    CHECKPOINT_PATH="crawler\sam_vit_h_4b8939.pth"
    sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH)
    mask_predictor = SamPredictor(sam)
    sam.to(device=DEVICE)
    mask_annotator = sv.MaskAnnotator(color=sv.Color.red())
    print("sam")
    rf = Roboflow(api_key="vt1WopMNT1DHN0D3Ml56")
    project = rf.workspace().project("yolo-m1mve")
    model = project.version(1).model
    print("robo")
    video_folder = os.listdir(path+"\\videos")
    print(video_folder)
    output_video = path+"\\annotated_video"
    os.makedirs(output_video)
    i=0
    for video in video_folder:
        print(video)
        cap = cv2.VideoCapture(os.path.join(path+"\\videos", video))
        print("vid extracted")
        
        
        # Define the path to save the frames
        save_path = f"crawler\\{i+1}"

        # Create the directory if it does not exist
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        output_path = os.path.join(output_video, f"{video}")
        print(output_path)
        cap_out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'),cap.get(cv2.CAP_PROP_FPS), (640, 640), isColor=True)
        # Loop through the frames and save them as JPEG files
        frame_count = 0
        
        object_timestamps={}
        predictions_list = []
        data = {
        "dataset info": {
            "name":dataset,
            "description": description_d,
            "contributor": author,
            "date_created": f"{creation_date}",
            "duration in seconds" : duration,
            "path":path
        },
        "video metadata":{
            "video title":video,
            "description": description_v,
            "duration in seconds" : duration,
            "views":views,
            "video format":video_format,
            "resolution":resolution,
            
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
                timestamp = frame_count / cap.get(cv2.CAP_PROP_FPS)
        
                # Check if this object has been seen before
                object_id = f"{classe}"
                if object_id in object_timestamps:
                    # This object has been seen before, update its end timestamp
                    object_timestamps[object_id][-1] = (object_timestamps[object_id][-1][0], timestamp)
                else:
                    # This is a new object, add it to the dictionary
                    object_timestamps[object_id] = [(timestamp, timestamp)]
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
                        # Append the prediction to the list
                predictions_list.append({
                    
                    'frame': frame_count,
                    'predictions': predictions,
                    'bounding_boxes': (int(x0), int(y0),int(x1), int(y1)),
                    
                    
                })

                detections = detections[detections.area == np.max(detections.area)]
                if detections:
                    segmented_image = mask_annotator.annotate(scene=frame_t.copy(), detections=detections)
                    cv2.imwrite("example_with_bounding_boxes.jpg", segmented_image)
                    cap_out.write(segmented_image)

                else: 
                    cv2.imwrite("example_with_bounding_boxes.jpg", frame_t)
                    cap_out.write(frame_t)
          
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
                

            
            print("done!!!!!")
        # Release the video capture object and close all windows
        
        cap.release()
        cap_out.release()
        cv2.destroyAllWindows()
        data['video'].append({
            "width": wh[0]['width'],
            "height": wh[0]['height']
        })
    
        # Extract filename without extension
        filename = os.path.splitext(os.path.basename(video))[0]
        # Specify folder path
        folder_path = path+"\\annotations"
        os.makedirs(folder_path)
        # Create JSON file path
        json_path = os.path.join(folder_path, filename + ".json")
        
        # Write predictions list to JSON file
        print(data)
        with open(json_path, 'w') as f:
            json.dump(data, f)

    return data