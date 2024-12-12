from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

model = YOLO('e:/New Folder/roboflow/runs/detect/train/weights/best.pt')

results = model('e:/New Folder/roboflow/chess-image1.jpg', save=True)

