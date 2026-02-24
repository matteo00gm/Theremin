"""
Encapsulates the MediaPipe Hand Landmarker logic for hand tracking and gesture recognition.
"""
import os
import math
import logging
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
PINCH_THRESHOLD = float(os.getenv("PINCH_THRESHOLD", 0.22))
MODEL_PATH = "hand_landmarker.task"

class HandTracker:
    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            logging.info("Downloading Hand Landmarker AI model...")
            urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        
        options = vision.HandLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path=MODEL_PATH),
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def process_frame(self, image_rgb):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        result = self.detector.detect(mp_image)
        
        if not result.hand_landmarks:
            return None

        landmarks = result.hand_landmarks[0]
        t, i = landmarks[4], landmarks[8]
        w, k = landmarks[0], landmarks[5]
        
        pinch_dist = math.hypot(t.x - i.x, t.y - i.y)
        hand_size = math.hypot(w.x - k.x, w.y - k.y)
        
        return {
            'x': (t.x + i.x) / 2.0,
            'y': (t.y + i.y) / 2.0,
            'is_pinched': (pinch_dist / (hand_size + 1e-6)) < PINCH_THRESHOLD,
            'thumb_px': (t.x, t.y),
            'index_px': (i.x, i.y)
        }