

import glob
import os
from roboflow import Roboflow 

import json
from time import sleep
from PIL import Image, ImageDraw
import io
import base64
import requests
from os.path import exists
import os, sys, re, glob


import roboflow
from ultralytics import YOLO
#roboflow login
#roboflow login
from roboflow import Roboflow
"""rf = Roboflow(api_key="vt1WopMNT1DHN0D3Ml56")
project = rf.workspace().project("yolo-9lug8")
model = project.version(1).model

# infer on a local image
print(model.predict("crawler\coolest-cars-feature.jpg", confidence=40, overlap=30).json())"""
#create project with yolo
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


print(version_number)
version = new_project.version(version_number)
new_project.upload("crawler\\two-cigarettes-13262319.jpg")
version.deploy(model_type='yolov8', model_path=f'C:\\Users\\nourh\\pfe_nourhene\\runs\\detect\\train\\')"""
#model=version.model
# Upload an image to Roboflow






#deal with user's dataset
"""id = new_project.id.split("/")[1]
rf = Roboflow(api_key="vt1WopMNT1DHN0D3Ml56")
project = rf.workspace().project(id)
model = project.version(version_number).model

print(model.predict("crawler\\two-cigarettes-13262319.jpg", confidence=40, overlap=30).json())"""





  



