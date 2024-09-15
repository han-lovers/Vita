from deepface import DeepFace
import matplotlib.pyplot as plt
import cv2
from glob import glob
import pandas as pd

backends = ["opencv", "ssd", "dlib", "mtcnn", "retinaface", "mediapipe"]

img1 = glob("*.jpg")
print(img1)