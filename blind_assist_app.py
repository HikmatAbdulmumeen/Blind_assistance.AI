import streamlit as st
import numpy as np
from PIL import Image
from gtts import gTTS
import time
import random

st.set_page_config(page_title="VoiceVision", layout="centered")

# Brown background
st.markdown("""
<style>
    .stApp {
        background: #8B4513;
    }
    .fullscreen-button {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: transparent;
        border: none;
        cursor: pointer;
        z-index: 9999;
    }
    .status-text {
        color: #FFF8DC;
        font-size: 24px;
        text-align: center;
        font-weight: bold;
        margin: 20px 0;
    }
    .objects-text {
        color: #FFD700;
        font-size: 18px;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# All 80 COCO objects
COCO_OBJECTS = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck",
    "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
    "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra",
    "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove",
    "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
    "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
    "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair dryer",
    "toothbrush"
]

# Initialize session state
if 'detection_active' not in st.session_state:
    st.session_state.detection_active = False

# Fullscreen click area
clicked = st.button(" ", key="fullscreen_click")
if clicked:
    st.session_state.detection_active = not st.session_state.detection_active
    st.rerun()

# Show current status
if st.session_state.detection_active:
    st.markdown("<p class='status-text'>🔊 LISTENING - Tap screen to stop</p>", unsafe_allow_html=True)
else:
    st.markdown("<p class='status-text'>👆 TAP ANYWHERE TO START</p>", unsafe_allow_html=True)

# Object detection when active
if st.session_state.detection_active:
    def detect_objects_demo():
        # Simulate detecting random objects from the 80 COCO objects
        detected = []
        
        # Always detect 0-3 people
        num_people = random.randint(0, 3)
        if num_people > 0:
            detected.append(f"{num_people} person{'s' if num_people > 1 else ''}")
        
        # Detect 2-4 other random objects
        other_objects = random.sample([obj for obj in COCO_OBJECTS if obj != "person"], random.randint(2, 4))
        detected.extend(other_objects)
        
        return detected
    
    def speak_detection(objects):
        if objects:
            # Create natural sentence
            if len(objects) == 1:
                message = f"I see {objects[0]}"
            else:
                message = f"I see {', '.join(objects[:-1])} and {objects[-1]}"
        else:
            message = "The area appears clear"
        
        # Speak the message
        try:
            tts = gTTS(text=message, lang='en', slow=False)
            tts.save("detection.mp3")
            st.audio("detection.mp3", autoplay=True)
        except:
            pass
        
        return message
    
    # Auto-capture and process
    img_buffer = st.camera_input(" ", label_visibility="collapsed", key="detection_cam")
    
    if img_buffer:
        # Process image
        detected_objects = detect_objects_demo()
        message = speak_detection(detected_objects)
        
        # Show detection results
        st.markdown(f"<p class='status-text'>🎯 {message}</p>", unsafe_allow_html=True)
        
        # Show detected objects list in gold color
        st.markdown(f"<p class='objects-text'>Detected: {', '.join(detected_objects)}</p>", unsafe_allow_html=True)
        
        # Continue after 4 seconds
        time.sleep(4)
        st.rerun()
    else:
        # Wait for camera
        time.sleep(2)
        st.rerun()

# Simple footer
st.markdown("""
<div style='text-align: center; color: #FFF8DC; margin-top: 50px;'>
    <p>Tap screen to start/stop detection</p>
</div>
""", unsafe_allow_html=True)
