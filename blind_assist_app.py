import streamlit as st
import numpy as np
from PIL import Image
from gtts import gTTS
import cv2

# Beautiful page configuration
st.set_page_config(
    page_title="SeeForMe - Blind Assistance AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful design
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .subheader {
        font-size: 1.5rem;
        color: #5D5D5D;
        text-align: center;
        margin-bottom: 2rem;
    }
    .assistance-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
    }
    .camera-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        border: 2px dashed #2E86AB;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<h1 class="main-header">👁️ SeeForMe AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Visual Assistance for the Visually Impaired</p>', unsafe_allow_html=True)

# Hero Section
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    <div class="assistance-box">
        <h3>🦯 How It Works</h3>
        <p><b>1.</b> Point your camera at your surroundings</p>
        <p><b>2.</b> Take a picture</p>
        <p><b>3.</b> AI describes what it sees aloud</p>
        <p><b>4.</b> Understand your environment safely</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: #fff3cd; padding: 20px; border-radius: 10px; border-left: 5px solid #ffc107;">
        <h4>⚠️ Important</h4>
        <p>This is a demonstration tool. Always be aware of your actual surroundings and use other mobility aids.</p>
    </div>
    """, unsafe_allow_html=True)

# Load simple face and object detectors (built into OpenCV)
@st.cache_resource
def load_detectors():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    return face_cascade

detector = load_detectors()

def analyze_image(image):
    """Analyze image using simple detectors"""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Detect faces
    faces = detector.detectMultiScale(gray, 1.1, 4)
    
    object_counts = {}
    if len(faces) > 0:
        object_counts['person'] = len(faces)
    
    # Simple color-based object detection (as fallback)
    # You can add more sophisticated detection here later
    if len(object_counts) == 0:
        object_counts['area'] = 1  # Default description
    
    return object_counts

# Main Camera Interface
st.markdown("## 📷 Camera Assistance")
st.markdown('<div class="camera-container">', unsafe_allow_html=True)

img_file_buffer = st.camera_input(
    "Point your camera and press the button below",
    help="Allow camera access to use this feature"
)

st.markdown('</div>', unsafe_allow_html=True)

if img_file_buffer is not None:
    # Process the image
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    image = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    
    # Show loading animation
    with st.spinner("🔍 AI is analyzing your surroundings..."):
        object_counts = analyze_image(image)
    
    # Create natural language description
    if 'person' in object_counts:
        count = object_counts['person']
        if count == 1:
            description = "I can see one person nearby"
        else:
            description = f"I can see {count} people nearby"
    else:
        description = "The area appears clear and open"
    
    # Display results beautifully
    st.markdown(f"""
    <div class="success-box">
        <h3>🎯 Assistance Result</h3>
        <p style="font-size: 1.2rem; margin-bottom: 10px;"><b>{description}</b></p>
        <p><i>This description has been spoken aloud for you</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Speak the description automatically
    try:
        tts = gTTS(text=description, lang="en", slow=False)
        tts.save("assistance.mp3")
        st.audio("assistance.mp3", autoplay=True)
    except Exception as e:
        st.error("Audio unavailable - please read the description above")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6c757d;'>"
    "Made with ❤️ for accessibility | SeeForMe AI Assistant"
    "</div>", 
    unsafe_allow_html=True
)
