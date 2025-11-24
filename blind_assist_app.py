import streamlit as st
import numpy as np
from PIL import Image
from gtts import gTTS
import io

# Beautiful page configuration
st.set_page_config(
    page_title="SeeForMe - Blind Assistance AI",
    page_icon="🦯",
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
    .demo-box {
        background-color: #e7f3ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
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

# Simple image analysis (no complex AI for now)
def analyze_image_simple(image):
    """Simple image analysis that works without OpenCV/TensorFlow"""
    # Convert to numpy array
    img_array = np.array(image)
    
    # Simple brightness analysis
    avg_brightness = np.mean(img_array)
    
    # Simple color analysis
    avg_red = np.mean(img_array[:, :, 0])
    avg_green = np.mean(img_array[:, :, 1])
    avg_blue = np.mean(img_array[:, :, 2])
    
    # Generate description based on simple analysis
    if avg_brightness < 50:
        return "The area appears dark, please be cautious"
    elif avg_brightness > 200:
        return "The area is very bright and well-lit"
    elif avg_red > avg_green and avg_red > avg_blue:
        return "Warm lighting detected in the area"
    elif avg_green > avg_red and avg_green > avg_blue:
        return "Natural green tones detected, possibly outdoors"
    else:
        return "The area appears clear and accessible"

# Demo object detection (simulated)
def get_demo_objects():
    """Return demo objects for demonstration purposes"""
    demo_objects = ["person", "chair", "table", "door"]
    import random
    detected = random.sample(demo_objects, random.randint(1, 2))
    return detected

# Main Camera Interface
st.markdown("## 📷 Camera Assistance")
st.markdown('<div class="camera-container">', unsafe_allow_html=True)

img_file_buffer = st.camera_input(
    "Point your camera and press the button below",
    help="Allow camera access to use this feature"
)

st.markdown('</div>', unsafe_allow_html=True)

if img_file_buffer is not None:
    # Process the image using PIL only
    image = Image.open(img_file_buffer)
    
    # Show loading animation
    with st.spinner("🔍 Analyzing your surroundings..."):
        # Simple analysis
        simple_description = analyze_image_simple(image)
        
        # Demo object detection
        demo_objects = get_demo_objects()
    
    # Create description
    if demo_objects:
        if len(demo_objects) == 1:
            description = f"I can see a {demo_objects[0]}. {simple_description}"
        else:
            objects_text = " and ".join(demo_objects)
            description = f"I can see {objects_text}. {simple_description}"
    else:
        description = simple_description
    
    # Display results beautifully
    st.markdown(f"""
    <div class="success-box">
        <h3>🎯 Assistance Result</h3>
        <p style="font-size: 1.2rem; margin-bottom: 10px;"><b>{description}</b></p>
        <p><i>This description has been spoken aloud for you</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo notice
    st.markdown("""
    <div class="demo-box">
        <h4>🎭 Demonstration Mode</h4>
        <p>This is a demonstration version. In a full implementation, this would use advanced AI to detect real objects in your environment.</p>
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
    "Made with ❤️ for accessibility | SeeForMe AI Assistant (Demo Version)"
    "</div>", 
    unsafe_allow_html=True
)
