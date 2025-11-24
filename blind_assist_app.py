
import streamlit as st
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
from gtts import gTTS

st.set_page_config(page_title="Blind Assistance AI", page_icon="🦯")
st.warning("🦯 BLIND ASSISTANCE AI - FOR DEMONSTRATION ONLY")
st.title(" Blind Assistance AI")

@st.cache_resource
def load_model():
    return hub.load("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2")

model = load_model()

CLASS_NAMES = ['person', 'bicycle', 'car', 'chair', 'dining table', 'tv', 'laptop', 'cell phone', 'book']

uploaded_file = st.file_uploader(" Upload a photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)
    
    image_np = np.array(image)
    image_tensor = tf.convert_to_tensor(image_np)[tf.newaxis, ...]
    detections = model(image_tensor)
    
    boxes = detections['detection_boxes'][0].numpy()
    classes = detections['detection_classes'][0].numpy().astype(int)
    scores = detections['detection_scores'][0].numpy()
    
    object_counts = {}
    for i in range(len(scores)):
        if scores[i] > 0.5 and classes[i] < len(CLASS_NAMES):
            obj_name = CLASS_NAMES[classes[i]]
            object_counts[obj_name] = object_counts.get(obj_name, 0) + 1
    
    if object_counts:
        description = "I detect " + ", ".join([f"{count} {obj}" for obj, count in object_counts.items()])
    else:
        description = "No objects detected"
    
    st.success(f"**ASSISTANCE:** {description}")
    
    try:
        tts = gTTS(text=description, lang='en', slow=False)
        tts.save("assist.mp3")
        st.audio("assist.mp3")
    except:
        st.write(" " + description)
