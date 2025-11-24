import streamlit as st
import numpy as np
from PIL import Image
from gtts import gTTS
import time

# Auto-configure for blind users
st.set_page_config(
    page_title="AudioVision - Voice-First Assistant",
    page_icon="🎧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Bold, high-contrast design for visibility
st.markdown("""
<style>
    /* Vibrant background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main container with high contrast */
    .main-container {
        background-color: #000000;
        padding: 40px;
        border-radius: 25px;
        border: 4px solid #00FF00;
        margin: 20px 0;
    }
    
    /* Large, bold text for low vision */
    .main-title {
        font-size: 4rem !important;
        color: #00FF00 !important;
        text-align: center;
        font-weight: 900;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px #000000;
    }
    
    .subtitle {
        font-size: 1.8rem !important;
        color: #FFFFFF !important;
        text-align: center;
        font-weight: 600;
        margin-bottom: 30px;
    }
    
    /* Voice instruction box */
    .voice-box {
        background-color: #FF6B35;
        padding: 30px;
        border-radius: 20px;
        border: 3px solid #FFFFFF;
        margin: 25px 0;
        text-align: center;
    }
    
    /* Status messages */
    .status-box {
        background-color: #000000;
        color: #00FF00;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #00FF00;
        font-size: 1.4rem;
        text-align: center;
        margin: 20px 0;
    }
    
    /* Camera area styling */
    .camera-area {
        background-color: #1a1a1a;
        padding: 30px;
        border-radius: 20px;
        border: 3px dashed #00FF00;
        margin: 25px 0;
    }
</style>
""", unsafe_allow_html=True)

# Main app content
st.markdown("""
<div class="main-container">
    <h1 class="main-title">🎧 AUDIOVISION</h1>
    <p class="subtitle">Voice-First Environmental Assistant</p>
</div>
""", unsafe_allow_html=True)

# Voice instructions (will be spoken first)
st.markdown("""
<div class="voice-box">
    <h2 style='color: white; font-size: 2rem; margin: 0;'>🎤 VOICE MODE ACTIVE</h2>
    <p style='color: white; font-size: 1.3rem; margin: 10px 0 0 0;'>
        Point your device and wait for audio guidance
    </p>
</div>
""", unsafe_allow_html=True)

# Initial voice greeting (auto-plays)
def speak_message(message):
    """Speak message aloud"""
    try:
        tts = gTTS(text=message, lang='en', slow=False)
        tts.save("greeting.mp3")
        st.audio("greeting.mp3", autoplay=True)
    except:
        pass

# Auto-greet when app loads
if 'greeted' not in st.session_state:
    speak_message("Audio Vision Assistant activated. Point your device camera and wait for environment analysis.")
    st.session_state.greeted = True

# Simple analysis function
def analyze_environment(image):
    """Simple environment analysis"""
    img_array = np.array(image)
    brightness = np.mean(img_array)
    
    if brightness < 50:
        return "Low light environment detected. Please proceed with caution."
    elif brightness > 200:
        return "Brightly lit area detected. Good visibility."
    else:
        return "Moderate lighting detected. Environment appears clear."

# Camera interface with auto-capture
st.markdown("""
<div class="camera-area">
    <h3 style='color: #00FF00; text-align: center;'>📷 ENVIRONMENT SCANNER</h3>
    <p style='color: white; text-align: center;'>Camera will auto-analyze when ready</p>
</div>
""", unsafe_allow_html=True)

# Camera with auto-processing
img_file_buffer = st.camera_input(
    " ",
    label_visibility="collapsed"
)

# Auto-process when image is captured
if img_file_buffer is not None:
    with st.spinner(""):
        # Show processing status
        st.markdown("""
        <div class="status-box">
            🔍 ANALYZING ENVIRONMENT... PLEASE WAIT
        </div>
        """, unsafe_allow_html=True)
        
        # Process image
        image = Image.open(img_file_buffer)
        analysis = analyze_environment(image)
        
        # Speak results immediately
        speak_message(analysis)
        
        # Display results
        st.markdown(f"""
        <div class="status-box">
            ✅ ANALYSIS COMPLETE
            <br><br>
            {analysis}
        </div>
        """, unsafe_allow_html=True)
        
        # Auto-reset after 8 seconds for continuous use
        time.sleep(8)
        st.rerun()

# Continuous operation instructions
st.markdown("""
<div style='background-color: #000000; padding: 20px; border-radius: 15px; border: 2px solid #FF6B35; margin-top: 20px;'>
    <h3 style='color: #FF6B35; text-align: center;'>♾️ CONTINUOUS MODE</h3>
    <p style='color: white; text-align: center; font-size: 1.1rem;'>
        Keep pointing your device - the app will continuously analyze and speak
    </p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; color: #FFFFFF; margin-top: 30px;'>
    <p style='font-size: 0.9rem;'>VOICE-FIRST ACCESSIBILITY TECHNOLOGY</p>
</div>
""", unsafe_allow_html=True)
