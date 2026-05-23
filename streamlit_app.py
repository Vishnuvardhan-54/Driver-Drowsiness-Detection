import streamlit as st
import os

st.title("Driver Drowsiness Detection System")

st.write("AI-based Driver Monitoring System")

# Start Button

if st.button("Start Detection"):
    os.system("python appdd.py")

# Info Box
st.info("This system detects driver drowsiness using AI.")

# Features
st.write("""
Features:
- Eye Closure Detection
- Head Pose Detection
- Alarm Alert
- Screenshot Capture
""")

# GitHub Link
st.markdown("[GitHub Repository](https://github.com/Vishnuvardhan-54/Driver-Drowsiness-Detection.git)")