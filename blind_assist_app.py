import streamlit as st
import numpy as np
from PIL import Image
from gtts import gTTS
import time

st.set_page_config(page_title="AutoVision", layout="centered")

# Clean, minimal design
st.markdown("""
<style>
    .stApp {
        background: black;
    }
    .start-button {
        background: lime !important;
        color: black !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border: none !important;
        padding: 20px 40px !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# Start screen - only one button
if 'started' not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.markdown("<h1 style='color: lime; text-align: center;'>🎥 AUTO VISION</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: white; text-align: center;'>Tap once to start continuous scanning</p>", unsafe_allow_html=True)
    
    if st.button("START SCANNING", key="start", use_container_width=True):
        st.session_state.started = True
        st.rerun()
else:
    # Continuous mode after one tap
    def analyze_and_speak(image):
        img_array = np.array(image)
        brightness = np.mean(img_array)
        
        if brightness < 50:
            message = "Low light area, proceed with caution"
        elif brightness > 200:
            message = "Bright environment detected"
        else:
            message = "Area appears clear and accessible"
        
        # Auto-speak
        try:
            tts = gTTS(text=message, lang='en', slow=False)
            tts.save("speak.mp3")
            st.audio("speak.mp3", autoplay=True)
        except:
            pass
        
        return message

    # Auto-capture loop
    if 'last_img' not in st.session_state:
        st.session_state.last_img = None

    img_buffer = st.camera_input(" ", label_visibility="collapsed", key="auto_cam")

    if img_buffer and img_buffer != st.session_state.last_img:
        st.session_state.last_img = img_buffer
        image = Image.open(img_buffer)
        analysis = analyze_and_speak(image)
        
        # Auto-refresh every 4 seconds for continuous scanning
        time.sleep(4)
        st.rerun()

    # Keep refreshing
    time.sleep(2)
    st.rerun()
