import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="Leaf AI Celebration", layout="centered")

# 🎨 Background Style
st.markdown("""
<style>
.stApp {
    background: linear-gradient(-45deg, #00c9ff, #92fe9d, #ff758c, #ff7eb3);
    background-size: 400% 400%;
    animation: gradient 8s ease infinite;
}

@keyframes gradient {
    0% {background-position: 0%}
    50% {background-position: 100%}
    100% {background-position: 0%}
}

.title {
    text-align:center;
    font-size:45px;
    font-weight:bold;
    color:white;
    text-shadow: 0 0 20px #00ffcc;
}

.card {
    background: rgba(255,255,255,0.2);
    padding:20px;
    border-radius:20px;
    text-align:center;
    margin-top:10px;
    backdrop-filter: blur(10px);
}

.blink {
    animation: blink 1s infinite;
}
@keyframes blink {
    50% {opacity:0;}
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🌿 Leaf AI Celebration System</p>', unsafe_allow_html=True)

# 📸 Camera Input (WORKING)
image = st.camera_input("📸 Take Leaf Photo")

if image is not None:

    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)

    st.image(frame, caption="Captured Image")

    # HSV detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_green = np.array([25, 40, 40])
    upper_green = np.array([90, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)

    green_pixels = np.sum(mask == 255)
    total_pixels = mask.size

    ratio = green_pixels / total_pixels
    confidence = int(ratio * 100)
    infection = 100 - confidence

    # 🎯 Result logic
    if ratio > 0.40:
        result = "Healthy Leaf"
        color = "lightgreen"
        alert = "Plant is Healthy"
        spray = "No spray needed"
    else:
        result = "Diseased Leaf"
        color = "red"
        alert = "Disease Detected!"
        spray = "Use Fungicide Spray"

    # Highlight diseased area
    disease_area = cv2.bitwise_not(mask)
    frame[disease_area > 0] = [0, 0, 255]

    st.image(frame, caption="Detection Result")

    # 🟢 HEALTHY MODE (CELEBRATION)
    if result == "Healthy Leaf":
        st.balloons()  # 🎉 celebration
        st.success("🎉 Healthy Leaf Detected!")

        st.markdown(f"""
        <div class='card'>
        <h2 style='color:{color}'>🌿 {result}</h2>
        <h3>Confidence: {confidence}%</h3>
        <h3>💊 {spray}</h3>
        </div>
        """, unsafe_allow_html=True)

    # 🔴 DISEASE MODE (ALERT)
    else:
        st.error("🚨 Disease Detected!")

        st.markdown("""
        <h1 class='blink' style='color:red; text-align:center;'>
        🚨 DANGER 🚨
        </h1>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='card'>
        <h2 style='color:{color}'>🍂 {result}</h2>
        <h3>Confidence: {confidence}%</h3>
        <h3>💊 {spray}</h3>
        </div>
        """, unsafe_allow_html=True)

    # 📊 Extra info
    st.write(f"Confidence: {confidence}%")
    st.write(f"Infection: {infection}%")
    st.write(f"Alert: {alert}")